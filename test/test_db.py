from sqlalchemy import text


def insert_user(db):
    db.execute(text("""
        INSERT INTO user 
            (idx, login_id,
            password,
            email,
            created_at, updated_at) 
        VALUES 
            (1, 'USER4', 'user4',
            b'$2b$12$J3ACyNOPIKTjQc4JFl2pVOIZRS1hxV3weOHS/qbffPqqzsqUoIqLC',
            'init@init.init',
            1, 1);
    """))
