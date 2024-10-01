import mysql.connector
import pandas as pd

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'ikman_product_database'
}

def get_statistics():
    # Connect to the database
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)

    # Query to get total products scraped
    cursor.execute("SELECT COUNT(*) AS total_products FROM products;")
    total_products = cursor.fetchone()['total_products']

    # Query to get average price by category
    cursor.execute("""
        SELECT category, AVG(price) AS average_price
        FROM products
        GROUP BY category;
    """)
    average_price_by_category = cursor.fetchall()

    # Query to get products that are out of stock
    cursor.execute("""
        SELECT name, category
        FROM products
        WHERE stock = 'Out of Stock';
    """)
    out_of_stock_products = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return total_products, average_price_by_category, out_of_stock_products

def save_statistics_to_csv(total_products, average_price_by_category, out_of_stock_products):
    # Create a DataFrame for the average prices by category
    avg_price_df = pd.DataFrame(average_price_by_category)

    # Save average price by category to CSV
    avg_price_df.to_csv('average_price_by_category.csv', index=False)
    
    # Create a summary DataFrame
    summary_data = {
        'Total Products Scraped': [total_products],
        'Out of Stock Products Count': [len(out_of_stock_products)]
    }
    summary_df = pd.DataFrame(summary_data)

    # Save the summary DataFrame to CSV
    summary_df.to_csv('summary_statistics.csv', index=False)

    # Save out of stock products to a CSV
    if out_of_stock_products:
        out_of_stock_df = pd.DataFrame(out_of_stock_products)
        out_of_stock_df.to_csv('out_of_stock_products.csv', index=False)

def main():
    total_products, average_price_by_category, out_of_stock_products = get_statistics()
    save_statistics_to_csv(total_products, average_price_by_category, out_of_stock_products)
    print('Statistics saved to CSV files.')

if __name__ == '__main__':
    main()
