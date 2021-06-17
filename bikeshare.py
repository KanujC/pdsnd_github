
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

LIST_OF_MONTHS = [ 'january','february','march','april','may','june','all']

LIST_OF_DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s Explore Some US\'s City\'s Bikeshare Data! ')
    city = input('Enter the City Name That You Would Like to Learn About: ').lower()
    while city not in CITY_DATA:
        print('Data Available is from City Among Chicago, NYC and Washington DC ')
        city = input('Enter the City Name That You Would Like to Learn About: ').lower()

    print('City That You Chose is: ', city)

   
    month = input("Data available is from January to June, Although you can also use the keyword 'all' to have all data of all the months: ").lower()
    while month not in LIST_OF_MONTHS:
        print('Please enter a valid month')
        month = input("Data available is from January to June, Although you can also use the keyword 'all' to have all data of all the months: ").lower()

    print('The Month You selected is: ',month)

   
    day = input("Enter the day of the week that you wish to view data about.Please enter 'all' if you wish to view data for all the days of the week:").lower()
    while day not in LIST_OF_DAYS:
        print('Please enter a valid day')
        day = input("Enter the day of the week that you wish to view data about.Please enter 'all' if you wish to view data for all the days of the week:").lower()

    print('The Day you selected is:', day)

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dFrame - Pandas DataFrame containing city data filtered by month and day
    """
  
    dFrame = pd.read_csv(CITY_DATA[city])

    dFrame['Start Time'] = pd.to_datetime(dFrame['Start Time'])
    dFrame['End Time'] = pd.to_datetime(dFrame['End Time'])
    dFrame['month'] = dFrame['Start Time'].dt.month
    dFrame['day_of_week'] = dFrame['Start Time'].dt.weekday_name
    dFrame['hour'] = dFrame['Start Time'].dt.hour

    if month != 'all':
  
        month = LIST_OF_MONTHS.index(month) +1

        dFrame = dFrame[dFrame['month'] == month]

    if day != 'all':
        dFrame = dFrame[dFrame['day_of_week'] == day.title()]

    return dFrame

def time_stats(dFrame):
    """Displays statistics on the most frequent times of travel."""

    print('Processing The Most Frequent Times of Travel...\n')
    start_time = time.time()
    popular_month_place = dFrame['Start Time'].dt.month.mode()[0]
    popular_month = LIST_OF_MONTHS[popular_month_place-1].title()
    print('The most popular month is:',popular_month)
    popular_day = dFrame['day_of_week'].mode()[0]
    print('Most popular day of the week is:',popular_day)
    popular_hour = dFrame['hour'].mode()[0]
    print('Most popular Start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(dFrame):
    """Displays statistics on the most popular stations and trip."""

    print('Processing The Most Popular Stations and Trip...\n')
    start_time = time.time()

   
    popular_start_station = dFrame['Start Station'].mode()[0]
    print('Most popular start station is', popular_start_station,'in city')
   
    popular_end_station = dFrame['End Station'].mode()[0]
    print('Most popular end station is', popular_end_station,'in city')
    
    popular_start_end_comination = dFrame.loc[:, 'Start Station':'End Station'].mode()[0:]
    print('The most popular combination of start and end station is\n',popular_start_end_comination)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(dFrame):
    """Displays statistics on the total and average trip duration."""

    print('\nProcessing Trip Duration...\n')
    start_time = time.time()

    dFrame['time difference'] = dFrame['End Time'] - dFrame['Start Time']
    total_time_difference = dFrame['time difference'].sum()
    print('the total travel time was:',total_time_difference)
    mean_travel_time = dFrame['time difference'].mean()
    print('the mean travel time was:', mean_travel_time)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(dFrame):
    """Displays statistics on bikeshare users."""

    print('Processing User Stats...\n')
    start_time = time.time()

    try:
        user_types = dFrame['User Type'].value_counts()
        print('The type and number of users in city are\n', user_types)
    except Exception as e:
        print('There was an error processing your request, plese look at all the inputs or try again later: {}'.format(e))

    try:
        gender_count = dFrame['Gender'].value_counts()
        print('The number of users and their genders:\n', gender_count)
    except Exception as e:
        print('The gender details for Washington is not available')

    try:
        earliest_year_of_birth = int(dFrame['Birth Year'].min())
        most_recent_year_of_birth = int(dFrame['Birth Year'].max())
        most_common_year_of_birth = int(dFrame['Birth Year'].mode())
        print('\nThe oldest customer was born in\n',earliest_year_of_birth,'\nthe youngest customer was born in\n',most_recent_year_of_birth,'\nthe most frequent customers were born in\n',most_common_year_of_birth)
    except Exception as e:
        print('The birth year details for Washington is not available')
    print("\nThis took %s seconds." % (time.time() - start_time))

def data_view(dFrame):
    wish=input('\nDo you wish to view 5 rows of raw data? Please enter yes or no\n').lower()
    while wish == 'yes':
        print(dFrame.head())
        wish=input('\nDo you wish to view 5 rows of raw data? Please enter yes or no\n').lower()
    else :
        return


def main():
    while True:
        city, month, day = get_filters()
        dFrame = load_data(city, month, day)

        time_stats(dFrame)
        station_stats(dFrame)
        trip_duration_stats(dFrame)
        user_stats(dFrame)
        data_view(dFrame)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
