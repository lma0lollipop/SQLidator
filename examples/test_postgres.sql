SELECT id, email, age
FROM users
WHERE email IS NOT NULL
  AND email <> ''
  AND email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
  AND age IS NOT NULL
  AND age >= 18;
