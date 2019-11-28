--List the following details of each employee: employee number, last name, first name, gender, and salary.
select e.emp_no, e.first_name, e.last_name, s.salary from employees as e
inner join salaries as s on e.emp_no = s.emp_no;

--List employees who were hired in 1986.
select * from employees where hire_date between '1986-01-01' and '1986-12-31';

--List the manager of each department with the following information: 
--department number, department name, the manager's employee number, 
--last name, first name, and start and end employment dates.
select dm.dept_no, d.dept_name, dm.emp_no, e.last_name, e.first_name, e.hire_date, dm.to_date
from dept_managers dm
join departments d on d.dept_no = dm.dept_no
join employees e on e.emp_no = dm.emp_no;


--List the department of each employee with the following information: 
--employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e
inner join dept_emp de on e.emp_no = de.emp_no
left join departments d on d.dept_no = de.dept_no;

--List all employees whose first name is "Hercules" and last names begin with "B."
select * from employees 
where first_name='Hercules' and last_name like 'B%';

--List all employees in the Sales department, including their 
--employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e 
inner join dept_emp de on e.emp_no = de.emp_no
inner join departments d on de.dept_no = d.dept_no
where d.dept_name = 'Sales';

--List all employees in the Sales and Development departments, 
--including their employee number, last name, first name, and department name.
select e.emp_no, e.last_name, e.first_name, d.dept_name
from employees e 
inner join dept_emp de on e.emp_no = de.emp_no
inner join departments d on de.dept_no = d.dept_no
where d.dept_name = 'Sales' or d.dept_name = 'Development'

--In descending order, list the frequency count of employee last names, 
--i.e., how many employees share each last name.
select last_name, count(last_name) as "Last Name Count" 
from employees
group by last_name
order by 2 desc;