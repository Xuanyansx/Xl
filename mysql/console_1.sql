show databases ;
use db6;
show tables ;
show create table dep;
desc dep;

select * from dep;
select * from emp;

select e.*,d.name from (select * from emp where salary=8000) as e join dep as d on e.dep_id = d.id;

select e.name,d.name from emp as e join dep as d on e.dep_id = d.id where e.salary = 8000;


-- 查询所有人的职级
select e.name,e.salary,j.grade from emp as e join job_grade as j on j.min_salary<=e.salary and e.salary<=j.max_salary;
select e.name,e.salary,j.grade from emp as e join job_grade as j on e.salary between j.min_salary and j.max_salary;

-- 查询人事部的职级
select e.name,d.name from emp as e join dep as d on e.dep_id = d.id where d.id = (select id from dep where name = '人事部');

select ee.*,j.grade
from (select e.* from emp as e join dep as d on e.dep_id = d.id where d.id = (select id from dep where name = '人事部')) as ee
         join job_grade as j on ee.salary between j.min_salary and j.max_salary;

-- 查询薪资低于部门平均值的员工

select avg(emp.salary),dep.name from emp  join dep on emp.dep_id = dep.id group by emp.dep_id;

select e.name,e.salary,avg_s.name
from emp as e
         join (select avg(emp.salary) as avg_sa, dep.*
               from emp
                        join dep on emp.dep_id = dep.id group by emp.dep_id)
             as avg_s on e.dep_id = avg_s.id where e.salary < avg_s.avg_sa;

-- 查询每个部门的员工数量

select count(emp.id),dep.name from emp join dep on emp.dep_id = dep.id group by emp.dep_id;

