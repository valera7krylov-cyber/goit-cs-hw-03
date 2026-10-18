-- 1. Отримати задачі для конкретного користувача з ID 3
SELECT *
FROM tasks
WHERE user_id = 3;


-- 2. Отримати задачі зі статусом "new"
SELECT *
FROM tasks
WHERE status_id = (
    SELECT id
    FROM status
    WHERE name = 'new'
);


-- 3. Оновити статус конкретного завдання (ID 1) на "in progress"
UPDATE tasks
SET status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
)
WHERE id = 1;


-- Завдання 4. Отримати список користувачів, які не мають жодного завдання
SELECT *
FROM users
WHERE id NOT IN (
    SELECT user_id
    FROM tasks
    WHERE user_id IS NOT NULL
);


-- Завдання 5. Додати нове завдання для конкретного користувача
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Prepare homework',
    'Description of the new task',
    (SELECT id FROM status WHERE name = 'new'),
    3  
);


-- Завдання 6. Отримати всі завдання, які ще не завершено
SELECT *
FROM tasks
WHERE status_id <> (
    SELECT id
    FROM status
    WHERE name = 'completed'
);


-- Завдання 7. Видалити конкретне завдання
DELETE FROM tasks
WHERE id = 2;


-- Завдання 8. Знайти користувачів з певною електронною поштою
SELECT *
FROM users
WHERE email LIKE '%@gmail.com';


-- Завдання 9. Оновити ім'я користувача
UPDATE users
SET fullname = 'Valerii Kovalenko'
WHERE id = 3;

-- Завдання 10. Отримати кількість завдань для кожного статусу
SELECT
    status.name,
    COUNT(tasks.id) AS task_count
FROM status
LEFT JOIN tasks ON tasks.status_id = status.id
GROUP BY status.id, status.name;

-- Завдання 11. Отримати завдання користувачів з певним доменом email
SELECT
    tasks.id,
    tasks.title,
    users.fullname,
    users.email
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@gmail.com';


-- Завдання 12. Отримати список завдань, що не мають опису
SELECT *
FROM tasks
WHERE description IS NULL;


-- Завдання 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
SELECT
    users.id,
    users.fullname,
    tasks.id AS task_id,
    tasks.title
FROM users
INNER JOIN tasks ON tasks.user_id = users.id
WHERE tasks.status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
);


-- Завдання 14. Отримати користувачів та кількість їхніх завдань
SELECT
    users.id,
    users.fullname,
    COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON tasks.user_id = users.id
GROUP BY users.id, users.fullname
ORDER BY users.id;