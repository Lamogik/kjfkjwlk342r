async def migration_db(db):

    await db.connect()

    await db.change("""
        CREATE TABLE IF NOT EXISTS lames ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            userid BIGINT,
            username TEXT,
            login TEXT,
            passwrd TEXT
        )
        """)

    await db.change("""
    CREATE TABLE IF NOT EXISTS leads ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        userid BIGINT,
        username TEXT,
        urlRef TEXT,
        sber TEXT,
        vtb TEXT,
        tin TEXT,
        alfa TEXT,
        count_of_accs INTEGER
    )
    """)

    await db.change("""
        CREATE TABLE IF NOT EXISTS users ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            userid BIGINT,
            username TEXT,
            balance REAL,
            wallet TEXT,
            methode INTEGER,
            totalCountAcc INTEGER,
            moderationCountAcc INTEGER,
            payedCountAcc INTEGER,
            urlRef TEXT,
            urlBot TEXT,
            count_of_lead INTEGER,
            views_balance REAL,
            leads_balance REAL
        )
        """)

    await db.change("""
    CREATE TABLE IF NOT EXISTS referrals ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        userid BIGINT,
        username TEXT,
        urlRef TEXT
    )
    """)

    await db.change("""
        CREATE TABLE IF NOT EXISTS accounts ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            userid BIGINT,
            username TEXT,
            tt_url TEXT,
            total_count_videos INTEGER,
            total_count_views INTEGER,
            total_count_subs INTEGER,
            total_count_likes INTEGER
        )
        """)

    await db.change("""
                CREATE TABLE IF NOT EXISTS moderationAccounts ( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    userid BIGINT,
                    tt_url TEXT
                )
                """)

    await db.change("""
            CREATE TABLE IF NOT EXISTS payedAccounts ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                userid BIGINT,
                tt_url TEXT
            )
            """)

    await db.change("""
                CREATE TABLE IF NOT EXISTS bannedUsers ( 
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    userid BIGINT
                )
                """)

    await db.change("""
                    CREATE TABLE IF NOT EXISTS admin ( 
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        userid BIGINT,
                        checker_status INTEGER,
                        payout_status INTEGER,
                        last_check_date TEXT
                    )
                    """)

    await db.close()

