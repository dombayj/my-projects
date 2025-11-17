import pandas as pd
import mysql.connector
from mysql.connector import Error
password =""
def get_filtered_urls():
    try:
        # MySQL database connection configuration
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="instagramurl"
            )
        
        if connection.is_connected():
            print("Connected to MySQL database")
            
            # Query to get URLs not present in urlstofollow
            query = """
                SELECT u.id, u.name, u.url 
                FROM urls u
                LEFT JOIN urlstofollow uf ON u.url = uf.url
                WHERE uf.url IS NULL 
                AND u.followerNumber >= 1000;
                """
            
            # Execute query and load into DataFrame
            filtered_df = pd.read_sql(query, connection)
            
            # Print statistics
            count_query = "SELECT COUNT(*) FROM urls"
            original_count = pd.read_sql(count_query, connection).iloc[0,0]
            
            count_query = "SELECT COUNT(*) FROM urlstofollow"
            to_follow_count = pd.read_sql(count_query, connection).iloc[0,0]
            
            print(f"Original URLs count: {original_count}")
            print(f"URLs to follow count: {to_follow_count}")
            print(f"Filtered URLs count: {len(filtered_df)}")
            
            return filtered_df
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None
        
    
# Get the filtered URLs
result_df = get_filtered_urls()

# Save to CSV if needed
if result_df is not None:
    result_df.to_csv('filtered_urls.csv', index=False)

    print("Results saved to filtered_urls.csv")
