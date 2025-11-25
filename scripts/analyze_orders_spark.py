from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, avg, sum as _sum, count as _count
)
from pymongo import MongoClient
import os

MONGO_URI = "mongodb://localhost:27017"
MONGO_DB_NAME = "food_delivery"
DETAILS_COLLECTION = "orders_detail"
CITY_AGG_COLLECTION = "city_metrics"
RESTAURANT_AGG_COLLECTION = "restaurant_metrics"


def get_mongo_collection(collection_name: str):
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    return db[collection_name]


def write_df_to_mongo(df, collection_name: str):
    """
    Writes a Spark DataFrame to MongoDB using foreachPartition.
    """
    def write_partition(partition):
        collection = get_mongo_collection(collection_name)
        docs = [row.asDict(recursive=True) for row in partition]
        if docs:
            collection.insert_many(docs)

    df.foreachPartition(write_partition)


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, "data", "raw", "food_orders.csv")

    spark = (
        SparkSession.builder
        .appName("FoodDeliveryAnalysis")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")

    # 1. Read CSV
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(input_path)
    )

    print("Schema of input data:")
    df.printSchema()

    # 2. Basic cleaning / type checks (already inferSchema, but we can enforce)
    df_clean = df.dropna(subset=["city", "restaurant_name", "final_amount"])

    # 3. Add derived columns
    df_enriched = (df_clean
        .withColumn(
            "avg_order_value_per_item",
            col("final_amount") / col("quantity")
        )
        .withColumn(
            "is_high_value_order",
            when(col("final_amount") >= 500, True).otherwise(False)
        )
    )

    # 4. Aggregation by city
    city_agg = (df_enriched
        .groupBy("city")
        .agg(
            _count("*").alias("num_orders"),
            _sum("final_amount").alias("total_revenue"),
            avg("final_amount").alias("avg_order_value"),
            avg("delivery_rating").alias("avg_rating")
        )
    )

    # 5. Aggregation by restaurant
    restaurant_agg = (df_enriched
        .groupBy("city", "restaurant_name")
        .agg(
            _count("*").alias("num_orders"),
            _sum("final_amount").alias("total_revenue"),
            avg("final_amount").alias("avg_order_value"),
            avg("delivery_rating").alias("avg_rating")
        )
    )

    # 6. Write detailed enriched orders to MongoDB
    print("Writing detailed orders to MongoDB...")
    write_df_to_mongo(df_enriched, DETAILS_COLLECTION)

    # 7. Write city-level metrics to MongoDB
    print("Writing city-level metrics to MongoDB...")
    write_df_to_mongo(city_agg, CITY_AGG_COLLECTION)

    # 8. Write restaurant-level metrics to MongoDB
    print("Writing restaurant-level metrics to MongoDB...")
    write_df_to_mongo(restaurant_agg, RESTAURANT_AGG_COLLECTION)

    print("Done! Check MongoDB for collections:")
    print(f" - {DETAILS_COLLECTION}")
    print(f" - {CITY_AGG_COLLECTION}")
    print(f" - {RESTAURANT_AGG_COLLECTION}")

    spark.stop()


if __name__ == "__main__":
    main()
