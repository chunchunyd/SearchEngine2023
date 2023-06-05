0 前言
SQLite数据库由于其简单、灵活、轻量、开源，已经被越来越多的被应用到中小型应用中。甚至有人说，SQLite完全可以用来取代c语言中的文件读写操作。因此我最近编写有关遥感数据处理的程序的时候，也将SQLite引入进来，以提高数据的结构化程度，并且提高大数据的处理能力（SQLite最高支持2PB大小的数据）。但是最开始，我发现，直接使用SQL语句的插入效率简直低的令人发指的。后来不断查文档、查资料，才发现了一条快速的“数据插入”之路。本文就以插入数据为例，整合网上和资料书中的各种提高SQLite效率的方法，给出提高SQLite数据插入效率的完整方法。（大神们勿喷）

1 数据

我使用的电脑是Win7 64位系统，使用VC2010编译，SQLIte版本为3.7.15.2 ，电脑CPU为二代i3处理器，内存6G。

实验之前，先建立要插入数据的表:

```sql
create table t1 (id integer , x integer , y integer， weight real)
```

2 慢速——最粗暴的方法

SQLite的API中直接执行SQL的函数是：

```c++
int sqlite3_exec(  sqlite3*,    const char *sql,   int (*callback)(void*,int,char**,char**),   void *,   char **errmsg)
```

直接使用INSERT语句的字符串进行插入，程序部分代码（完整代码见后文），如下：
```c++
for(int i=0;i<nCount;++i)
{
	std::stringstream ssm;
	ssm<<"insert into t1 values("<<i<<","<<i*2<<","<<i/2<<","<<i*i<<")";
	sqlite3_exec(db,ssm.str().c_str(),0,0,0);
}
```

这个程序运行的太慢了，我已经没时间等待了，估算了一下，基本上是  7.826 条/s

3 中速——显式开启事务

所谓”事务“就是指一组SQL命令，这些命令要么一起执行，要么都不被执行。在SQLite中，**每调用一次sqlite3_exec()函数，就会隐式地开启了一个事务**，如果插入一条数据，就调用该函数一次，事务就会被反复地开启、关闭，会增大IO量。如果在插入数据前显式开启事务，插入后再一起提交，则会大大提高IO效率，进而加数据快插入速度。

开启事务只需在上述代码的前后各加一句开启与提交事务的命令即可：

```c++
sqlite3_exec(db,"begin;",0,0,0);
for(int i=0;i<nCount;++i)
{
	std::stringstream ssm;
	ssm<<"insert into t1 values("<<i<<","<<i*2<<","<<i/2<<","<<i*i<<")";
	sqlite3_exec(db,ssm.str().c_str(),0,0,0);
}
sqlite3_exec(db,"commit;",0,0,0);
```

显式开启事务后，这个程序运行起来明显快很多，估算效率达到了34095条/s，较原始方法提升约5000倍。



4 高速——写同步(synchronous)

我要使用一个遥感处理算法处理10000*10000的影像，中间有一步需要插入100000000条数据到数据库中，如果按照开启事务后的速度34095条/s，则需要100000000÷34095 = 2932秒 = 48.9分，仍然不能够接受，所以我接着找提升速度的方法。终于，在有关讲解SQLite配置的资料中，看到了“写同步”选项。

在SQLite中，数据库配置的参数都由编译指示（pragma）来实现的，而其中synchronous选项有三种可选状态，分别是full、normal、off。这篇博客以及官方文档里面有详细讲到这三种参数的设置。简要说来，full写入速度最慢，但保证数据是安全的，不受断电、系统崩溃等影响，而off可以加速数据库的一些操作，但如果系统崩溃或断电，则数据库可能会损毁。

SQLite3中，该选项的默认值就是full，如果我们再插入数据前将其改为off，则会提高效率。如果仅仅将SQLite当做一种临时数据库的话，完全没必要设置为full。在代码中，设置方法就是在打开数据库之后，直接插入以下语句：

```c++
sqlite3_exec(db,"PRAGMA synchronous = OFF; ",0,0,0);
```

此时，经过测试，插入速度已经变成了 41851条/s，也就是说，插入100000000条数据，需要2389秒 = 39.8分。

5 极速——执行准备

虽然写同步设为off后，速度又有小幅提升，但是仍然较慢。我又一次踏上了寻找提高SQLite插入效率方法的道路上。终于，我发现，SQLite执行SQL语句的时候，有两种方式：一种是使用前文提到的函数sqlite3_exec()，该函数直接调用包含SQL语句的字符串；另一种方法就是“执行准备”（类似于存储过程）操作，即先将SQL语句编译好，然后再一步一步（或一行一行）地执行。如果采用前者的话，就算开起了事务，SQLite仍然要对循环中每一句SQL语句进行“词法分析”和“语法分析”，这对于同时插入大量数据的操作来说，简直就是浪费时间。因此，要进一步提高插入效率的话，就应该使用后者。

“执行准备”主要分为三大步骤：

1.调用函数

```c++
int sqlite3_prepare_v2( sqlite3 *db,  const char *zSql,  int nByte,  sqlite3_stmt **ppStmt,  const char **pzTail);
```

并且声明一个指向sqlite3_stmt对象的指针，该函数对参数化的SQL语句zSql进行编译，将编译后的状态存入ppStmt中。

2.调用函数 sqlite3_step() ，这个函数就是执行一步（本例中就是插入一行），如果函数返回的是SQLite_ROW则说明仍在继续执行，否则则说明已经执行完所有操作；

3.调用函数 sqlite3_finalize()，关闭语句。

关于执行准备的API的具体语法，详见官方文档。本文中执行准备的c++代码如下：

```c++
sqlite3_exec(db,"begin;",0,0,0);
	sqlite3_stmt *stmt;
	const char* sql = "insert into t1 values(?,?,?,?)";
	sqlite3_prepare_v2(db,sql,strlen(sql),&stmt,0);
	
	for(int i=0;i<nCount;++i)
	{		
		sqlite3_reset(stmt);
		sqlite3_bind_int(stmt,1,i);
		sqlite3_bind_int(stmt,1,i*2);
		sqlite3_bind_int(stmt,1,i/2);
		sqlite3_bind_double(stmt,1,i*i);
	}
	sqlite3_finalize(stmt);
	sqlite3_exec(db,"commit;",0,0,0);
```

此时测试数据插入效率为： 265816条/s，也就是说，插入100000000条数据，需要376秒 = 6.27分。这个速度已经很满意了。

5 总结

综上所述啊，SQLite插入数据效率最快的方式就是：事务+关闭写同步+执行准备（存储过程），如果对数据库安全性有要求的话，就开启写同步。