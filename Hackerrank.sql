# Julia conducted a  days of learning SQL contest. The start date of the contest was March 01, 2016 and the end date was March 15, 2016.

# Write a query to print total number of unique hackers who made at least  submission each day (starting on the first day of the contest),
# and find the hacker_id and name of the hacker who made maximum number of submissions each day. If more than one such hacker has a maximum number of submissions,
# print the lowest hacker_id. The query should print this information for each day of the contest, sorted by the date.

-- max submissions per date and hacker
with _hacker as
    (select submission_date, hacker_id , cnt, row_number() over(partition by submission_date order by cnt desc, hacker_id) as rn
    from
-- nb of submission per day and hacker
        (select submission_date, hacker_id, count(submission_id) as cnt
        from submissions
        group by submission_date, hacker_id) s
    where cnt>0),

-- number of submissions per date
_date as
    (select submission_date, count(hacker_id) as ct from
        (select submission_date, hacker_id, row_number() over(partition by hacker_id order by submission_date) as rd
        from a
        ) g
    where rd=day(submission_date)
    group by submission_date)

select a.submission_date, b.ct, a. hacker_id, h.name
from _hacker
join _date
    on a.submission_date=b.submission_date
left join hackers h
    on a.hacker_id=h.hacker_id
where a.rn=1
order by submission_date;