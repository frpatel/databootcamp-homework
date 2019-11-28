drop table if exists departments;
drop table if exists employees;
drop table if exists dept_emp;
drop table if exists dept_managers;
drop table if exists salaries;
drop table if exists titles;

create table departments(
	dept_no varchar(4) primary key,
	dept_name varchar(20)
);

create table employees(
	emp_no int primary key,
	birth_date date,
	first_name varchar(15),
	last_name varchar(15),
	gender char(1),
	hire_date date
);

create table dept_emp(
	emp_no int,
	dept_no varchar(4),
	from_date date,
	to_date date,
	foreign key (emp_no) references employees(emp_no),
	foreign key (dept_no) references departments(dept_no)
);

create table dept_managers(
	dept_no varchar(4),
	emp_no int,
	from_date date,
	to_date date,
	foreign key (emp_no) references employees(emp_no),
	foreign key (dept_no) references departments(dept_no)
);

create table salaries(
	emp_no int,
	salary int,
	from_date date,
	to_date date,
	foreign key (emp_no) references employees(emp_no)
);

create table titles(
	emp_no int,
	title varchar(20),
	from_date date,
	to_date date,
	foreign key (emp_no) references employees(emp_no)
);