import sqlite3
import pandas as pd

if __name__ == "__main__":
    conn = sqlite3.connect('file:cachedb?mode=memory&cache=shared')
    cur = conn.cursor()

    prod = pd.read_csv('products.csv')
    prod.to_sql("products", conn, if_exists='replace')

    ing = pd.read_csv('ingredients.csv')
    ing.to_sql('ingredients', conn, if_exists='replace')

    cur.execute("""
        SELECT
             P1.PRODUCT_NAME, P1.VERSION, P2.PRODUCT_NAME, P2.VERSION
        FROM
            (((SELECT
                 PRODUCT_NAME, VERSION, MAX(PRODUCT_ID) AS PRODUCT_ID
            FROM
                products
            GROUP BY PRODUCT_NAME) as P1
            INNER JOIN ingredients ON P1.PRODUCT_ID=ingredients.PRODUCT_ID)
            INNER JOIN products as P2 ON P2.PRODUCT_ID=ingredients.INGREDIENT_ID)
    """)

    # cur.execute("""
    #     SELECT
    #          PRODUCT_NAME, VERSION, MAX(PRODUCT_ID)
    #     FROM
    #         products
    #     GROUP BY PRODUCT_NAME
    # """)

    rows = cur.fetchall()
    for row in rows:
        print(row)
