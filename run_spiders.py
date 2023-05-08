from ecommerce_crawler.ecommerce_crawler.spiders.ecommerce_spider import run_spider

output_file = "ecommerce_crawler/output.json"

# Clear the output file
with open(output_file, 'w') as file:
    pass

# Run the spider
run_spider(output_file)

