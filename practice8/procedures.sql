CREATE TABLE IF NOT EXISTS incorrect_contacts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE OR REPLACE PROCEDURE upsert_contact(
    p_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM phonebook
        WHERE name = p_name
    ) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    IF array_length(p_names, 1) IS DISTINCT FROM array_length(p_phones, 1) THEN
        RAISE EXCEPTION 'All arrays must have the same length';
    END IF;

    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] ~ '^[0-9]{11}$' THEN
            CALL upsert_contact(
                p_names[i]::VARCHAR,
                p_phones[i]::VARCHAR
            );
        ELSE
            INSERT INTO incorrect_contacts(name, phone, error_message)
            VALUES (
                p_names[i],
                p_phones[i],
                'Invalid phone format. Phone must contain exactly 11 digits.'
            );

            RAISE NOTICE 'Incorrect data: %, %',
                p_names[i], p_phones[i];
        END IF;
    END LOOP;
END;
$$;


CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_value
       OR phone = p_value;
END;
$$;