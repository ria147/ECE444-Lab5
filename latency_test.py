import requests
import pandas as pd
import time
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt

# Function to perform latency testing
def perform_latency_test(base_url, endpoint, num_calls=100):
    start_timestamps, end_timestamps, latencies, api_calls = [], [], [], []

    for i in range(num_calls):
        start_time = time.time()  # Start timestamp
        start_timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
        response = requests.get(f"{base_url}{endpoint}")
        end_time = time.time()  # End timestamp
        end_timestamps.append(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))

        #Calculate difference = latency
        latency = end_time - start_time

        latencies.append(latency)
        api_calls.append(i+1)
    
    return start_timestamps, end_timestamps, latencies, api_calls

# Generate boxplots
def create_boxplot(filenames):
    # Initialize empty DataFrame to store all the results of all tests
    all_results = pd.DataFrame()

    # Load each csv file and add a new column for each test case
    for i, file in enumerate(filenames, start=1):
        df = pd.read_csv(file)
        df['test_case'] = f'Test Case {i}' # label each test case
        all_results = pd.concat([all_results, df], ignore_index=True)

    # Calculate average performance for each test case
    average_latencies = all_results.groupby('test_case')['Latency'].mean().reset_index()

    # Generate boxplot
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='test_case', y='Latency', data=all_results)
    plt.title('API Latency Boxplot for Test Cases')
    plt.xlabel('Test Case')
    plt.ylabel('Latency (seconds)')
    plt.xticks(rotation=45)  # Rotate x-axis labels if necessary
    
    # Annotate the plot with average latencies
    for i, row in average_latencies.iterrows():
        plt.text(i, row['Latency'], f"{row['Latency']:.5f}", ha='center', va='bottom', fontsize=10, color='red')
    
    plt.tight_layout()  # Adjust layout
    plt.savefig('latency_boxplot.png')  # Save the figure
    plt.show()

    
def main():
    print("Performing Latency tests:")
    # Define the AWS Elastic Beanstalk server
    base_url = "http://ece444pra5-env.eba-qtc3myge.ca-central-1.elasticbeanstalk.com/"

    # Define the test cases
    testcases = [
        "UofT is the best university in Canada", 
        "Aliens discovered in Mars", 
        "TTC Line 1 is not working", 
        "Eating rice causes cancer"
        ]

    # Define file names based on prediction/classifications
    filenames = [
        "real_news_1.csv",
        "fake_news_1.csv", 
        "real_news_2.csv",
        "fake_news_2.csv"
    ]
    
    # Run latency test for each test case
    for i in range(len(testcases)):
        print("Test case ", i+1, " : ", testcases[i])
        headline = testcases[i].replace(' ', '+')
        endpoint = "/?query="+headline
        start_timestamps, end_timestamps, latencies, api_calls = perform_latency_test(base_url=base_url, endpoint=endpoint)

        df_results = pd.DataFrame(
            {'API Call' : api_calls,
             'Start Time' : start_timestamps,
             'End Time' : end_timestamps,
             'Latency' : latencies
            })

        # save results in a csv file
        df_results.to_csv(filenames[i], index=False)
    
    print("Finished tests.")
    print("Generating boxplot for latencies and their averages")
    
    create_boxplot(filenames=filenames)
    print("Boxplot generated.")

if __name__ == "__main__":
    main()