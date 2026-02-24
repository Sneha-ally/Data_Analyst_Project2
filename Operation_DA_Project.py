import pandas as pd
df = pd.read_csv("customer_support_tickets.csv")
print(df.shape) #check rows and columns
print(df.head()) # check preview first 5rows
print(df.info()) # check column type
print(df.columns)
print(df.dtypes)
df.head()

# Clean column names: lowercase, remove spaces
df.columns = (
    df.columns
    .str.strip()                 # remove extra spaces
    .str.lower()                 # convert to lowercase
    .str.replace(" ", "_")       # replace space with underscore
)

# Verify cleaned column names
print(df.columns)
#missing values in each column
missing_values = df.isnull().sum()
print("Missing values in each column:")
print(missing_values)

#check ticket status count
df['ticket_status'].value_counts()

#check how many open tickets have missing resolution
df[df['ticket_status']!='Closed']['time_to_resolution'].isnull().sum()

#insted of filling values we will use flags to identify ticket is closed
df['is_closed'] = df['ticket_status'].apply(lambda x:1 if x == 'Closed' else 0)

# Flag to check if satisfaction is given
df['has_satisfaction'] = df['customer_satisfaction_rating'].apply(lambda x:0 if pd.isna(x) else 1)
# Flag for first response
df['response_received'] = df['first_response_time'].apply(
    lambda x: 0 if pd.isna(x) else 1

)

#resolution time only make sense for closed tickets
df.loc[df['is_closed'] == 0,'resolution_time_hours'] = None

# Age range check
print(df['customer_age'].min(), df['customer_age'].max())

# Convert categorical text columns to category type
categorical_cols = [
    'customer_gender',
    'ticket_status',
    'ticket_type',
    'ticket_priority',
    'ticket_channel',
    'product_purchased'
]

for col in categorical_cols:
    df[col] = df[col].astype('category')

    # Convert date of purchase (DD-MM-YYYY format)
    df['date_of_purchase'] = pd.to_datetime(
        df['date_of_purchase'],
        format='%d-%m-%Y',
        errors='coerce'
    )

    # Convert first response time (date + time)
    df['first_response_time'] = pd.to_datetime(
        df['first_response_time'],
        errors='coerce'
    )

    # Convert time to resolution (date + time)
    df['time_to_resolution'] = pd.to_datetime(
        df['time_to_resolution'],
        errors='coerce'
    )
    print(df[['first_response_time', 'time_to_resolution']].dtypes)

         # Create resolution time in hours
         # This calculates the difference between resolution time and first response time
    df['resolution_time_hours'] = (
                                          df['time_to_resolution'] - df['first_response_time']
                                  ).dt.total_seconds() / 3600

# Set resolution time to NaN for tickets that are not closed
df.loc[df['ticket_status'] != 'Closed', 'resolution_time_hours'] = None

print(df['resolution_time_hours'].head())

df[df['ticket_status'] == 'Closed'][['first_response_time', 'time_to_resolution', 'resolution_time_hours']].head()

# Final check
print(df.isnull().sum())

print(df.dtypes)

# Save the final cleaned dataset to a new CSV file
df.to_csv(
    "final_cleaned_customer_support_tickets.csv",
    index=False
)
#EDA(Exploratory Data Analysis)step 1
#Total number of tickets
total_tickets = df.shape[0]
print("Total number of tickets",total_tickets)

#Ticket Status Distribution
#Count tickets by status
ticket_status_count = df['ticket_status'].value_counts()

print(ticket_status_count)

#Ticket Type Distribution
#count tickets by type
ticket_type_count = df['ticket_type'].value_counts()
print(ticket_type_count)

#Ticket Priority Analysis
#count ticket by priority
ticket_priority_count =df['ticket_priority'].value_counts()
print(ticket_priority_count)

#Ticket Channel Analysis
#distribution of ticket by channel
ticket_channel_count = df['ticket_channel'].value_counts()
print(ticket_channel_count)

#EDA step 2
#Time-Based Analysis(peak hours )
#Tickets Over Time (by Month)
#Create year-month column for trend analysis
df['purchase_year_month'] =df['date_of_purchase'].dt.to_period('M')
#count number of tickets per month
tickets_per_month = df.groupby('purchase_year_month').size()
print(tickets_per_month)


#Tickets by Day of Week (Workload Planning)
#extrack day of week from purchase date
df['purchase_day'] = df['date_of_purchase'].dt.day_name()
#count ticket by day of week
tickets_by_day = df['purchase_day'].value_counts()
print(tickets_by_day)

#First Response Time – Hour Analysis(agents respond most
#Extract hour from first response time
df['response_hour'] = df['first_response_time'].dt.hour
#count response by hours
responses_by_hour = df['response_hour'].value_counts().sort_index()
print(responses_by_hour)

#import matplotlib.pyplot as plt

#Step 2 EDA| Bivariate Analysis|How does one variable affect another
print("Average resolution time (hours) by ticket priority:")
print(
    df.groupby('ticket_priority',observed=True)['resolution_time_hours']
      .mean()
      .sort_values()
)

#Ticket Status vs Customer Satisfaction
#rating
print("\nAverage customer satisfaction by ticket status:")
print(
    df.groupby('ticket_status',observed=True)['customer_satisfaction_rating']
      .mean()
)
#Identify which support channel responds fastest.(Ticket Channel vs First Response Time)

print("\nAverage first response time by ticket channel:")
print(
    df.groupby('ticket_channel',observed=True)['first_response_time']
      .mean()
)
#Ticket Type vs Resolution Time(finding which type of ticket takes the longest to resolve).
print("\nAverage resolution time (hours) by ticket type:")
print(
    df.groupby('ticket_type',observed=True)['resolution_time_hours']
      .mean()
      .sort_values(ascending=False)
)

#Check if customer age impacts satisfaction(Customer Age Group vs Satisfaction).
df['age_group'] = pd.cut(
    df['customer_age'],
    bins=[18, 25, 35, 45, 55, 65],
    labels=['18-25', '26-35', '36-45', '46-55', '56-65']
)

print("\nAverage customer satisfaction by age group:")
print(
    df.groupby('age_group',observed=True)['customer_satisfaction_rating']
      .mean()
)
#Ensure resolution time exists mainly for closed tickets.
print("\nAverage resolution time (hours) by closed status:")
print(
    df.groupby('is_closed',observed=True)['resolution_time_hours']
      .mean()
)
#Channel Performance Analysis
#count number of tickets by Channel
print("Ticket count by channel:")
print(df['ticket_channel'].value_counts())
#Average Resolution Time by Channel
#Average Resolution Time by ticket Channel
print("Average resolution time (hours) by channel:")
print(
    df.groupby('ticket_channel',observed=True)['resolution_time_hours']
    .mean()
     .sort_values()
)
#Average Customer Satisfaction by Channel
#Average Customer Satisfaction rating by Channel
print("Average Satisfaction rating by Channel:")
print(
    df.groupby('ticket_channel',observed=True)['customer_satisfaction_rating']
     .mean()
      .sort_values(ascending=False)
)
#percentage of closed tickets by channel
print("closed ticket percentage by channel:")
print(
      df.groupby('ticket_channel',observed=True)['is_closed']
       .mean()
        .sort_values(ascending=False)
)
# STEP : Combined channel performance metrics

channel_performance = df.groupby('ticket_channel', observed=True).agg(
    total_tickets=('ticket_id', 'count'),
    avg_resolution_time=('resolution_time_hours', 'mean'),
    avg_satisfaction=('customer_satisfaction_rating', 'mean'),
    closure_rate=('is_closed', 'mean')
)

print("Channel Performance Summary:")
print(channel_performance.sort_values(by='total_tickets', ascending=False))

print('age group distribution:')
print(df['age_group'].value_counts())
#  Number of tickets by age group

print("Ticket count by age group:")
print(
    df.groupby('age_group', observed=True)['ticket_id']
      .count()
      .sort_values(ascending=False)
)
#  Average resolution time by age group

print("Average resolution time (hours) by age group:")
print(
    df.groupby('age_group', observed=True)['resolution_time_hours']
      .mean()
      .sort_values()
)
#  Average satisfaction rating by age group

print("Average satisfaction rating by age group:")
print(
    df.groupby('age_group', observed=True)['customer_satisfaction_rating']
      .mean()
      .sort_values(ascending=False)
)
#  Ticket distribution by gender

#  Average resolution time by gender

print("Average resolution time (hours) by gender:")
print(
    df.groupby('customer_gender', observed=True)['resolution_time_hours']
      .mean()
      .sort_values()
)

#  Average satisfaction rating by gender

print("Average satisfaction rating by gender:")
print(
    df.groupby('customer_gender', observed=True)['customer_satisfaction_rating']
      .mean()
      .sort_values(ascending=False)
)
#Product-Level Performance Analysis||Ticket Count by Product

print("Ticket count by product:")
print(
    df['product_purchased']
      .value_counts()
      .sort_values(ascending=False)
)
#  Average resolution time (hours) by product

print("Average resolution time (hours) by product:")
print(
    df.groupby('product_purchased', observed=True)['resolution_time_hours']
      .mean()
      .sort_values(ascending=False)
)
# Average customer satisfaction rating by product

print("Average satisfaction rating by product:")
print(
    df.groupby('product_purchased', observed=True)['customer_satisfaction_rating']
      .mean()
      .sort_values()
)
#  Percentage of closed tickets by product

print("Closure rate by product:")
print(
    df.groupby('product_purchased', observed=True)['is_closed']
      .mean()
      .sort_values(ascending=False)
)
# Combined product-level performance metrics

product_performance = df.groupby('product_purchased', observed=True).agg(
    total_tickets=('ticket_id', 'count'),
    avg_resolution_time=('resolution_time_hours', 'mean'),
    avg_satisfaction=('customer_satisfaction_rating', 'mean'),
    closure_rate=('is_closed', 'mean')
)

print("Product Performance Summary:")
print(product_performance.sort_values(by='total_tickets', ascending=False))

#  Define SLA hours based on ticket priority

def get_sla_hours(priority):
    if priority == 'Critical':
        return 24
    elif priority == 'High':
        return 48
    elif priority == 'Medium':
        return 72
    else:
        return 96  # Low priority

# Create SLA column
df['sla_hours'] = df['ticket_priority'].apply(get_sla_hours)

print("SLA hours assigned based on priority:")
print(df[['ticket_priority', 'sla_hours']].head())

# Check datatypes of involved columns

print("Data types check:")
print(df[['resolution_time_hours', 'sla_hours']].dtypes)
# Convert SLA hours to numeric (important fix)

df['sla_hours'] = pd.to_numeric(df['sla_hours'], errors='coerce')

# Convert resolution time to numeric (safety check)

df['resolution_time_hours'] = pd.to_numeric(df['resolution_time_hours'], errors='coerce')

print("Fixed data types:")
print(df[['resolution_time_hours', 'sla_hours']].dtypes)

# Create SLA breach flag (1 = breached, 0 = within SLA)

df['sla_breached'] = (df['resolution_time_hours'] > df['sla_hours']).astype(int)

print("SLA breach distribution:")
print(df['sla_breached'].value_counts())

#  Calculate overall SLA breach percentage

sla_breach_rate = df['sla_breached'].mean() * 100

print("Overall SLA Breach Percentage:")
print(round(sla_breach_rate, 2), "%")

# STEP 7.4: SLA breach percentage by priority

print("SLA breach rate by ticket priority:")
print(
    df.groupby('ticket_priority', observed=True)['sla_breached']
      .mean()
      .sort_values(ascending=False) * 100
)
#  SLA breach percentage by channel

print("SLA breach rate by channel:")
print(
    df.groupby('ticket_channel', observed=True)['sla_breached']
      .mean()
      .sort_values(ascending=False) * 100
)
#  SLA performance summary

sla_summary = df.groupby('ticket_priority', observed=True).agg(
    total_tickets=('ticket_id', 'count'),
    breach_rate=('sla_breached', 'mean')
)

print("SLA Summary by Priority:")
print(sla_summary.sort_values(by='breach_rate', ascending=False))


df['is_closed'].value_counts()

total_tickets = len(df)
closed_tickets = df[df['is_closed'] == 1].shape[0]

closure_rate = (closed_tickets / total_tickets) * 100
print(f"Closure Rate: {closure_rate:.2f}%")





