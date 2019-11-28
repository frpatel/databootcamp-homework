select e.emp_no, e.first_name, e.last_name, s.salary from employees as e
inner join salaries as s on e.emp_no = s.emp_no;

select * from employees where hire_date between '1986-01-01' and '1986-12-31';

select dm.dept_no, d.dept_name, dm.emp_no, e.last_name, e.first_name, e.hire_date, dm.to_date
from dept_managers dm
join departments d on d.dept_no = dm.dept_no
join employees e on e.emp_no = dm.emp_no;

select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e
inner join dept_emp de on e.emp_no = de.emp_no
left join departments d on d.dept_no = de.dept_no;

select * from employees 
where first_name='Hercules' and last_name like 'B%';

select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e 
inner join dept_emp de on e.emp_no = de.emp_no
inner join departments d on de.dept_no = d.dept_no
where d.dept_name = 'Sales';

select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e 
inner join dept_emp de on e.emp_no = de.emp_no
inner join departments d on de.dept_no = d.dept_no
where d.dept_name = 'Sales' or d.dept_name = 'Development'

select last_name, count(last_name) as "Last Name Count" 
from employees
group by last_name
order by 2 desc;