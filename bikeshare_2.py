import time
import pandas as pd
import numpy as np

#If this code is changed, please update README.md to make sure features.

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid input
    while True:
        city = input('Which city dou you want to explore? : ').lower()
        if city not in CITY_DATA:
            print("You can input only {}, {}, {}".format(*CITY_DATA.keys()))
            continue

        break

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = input('Which month? :').lower()

        if month not in months:
            print("You can input only {},{},{},{},{},{},{}".format(*months))
            continue

        break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('Which week of day? :').lower()

        if day not in days:
            print("You can input only {},{},{},{},{},{},{},{}".format(*days))
            continue

        break

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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_DATA.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    popular_month = df['month'].value_counts().index[0]
    print('The most frequent month: ', MONTH_DATA[popular_month -1 ])

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].value_counts().index[0]
    print('The most frequent day of week: ', popular_day_of_week)

    # display the most common start hour
    popular_hour = df['hour'].value_counts().index[0]
    print('The most frequent hour: ', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().index[0]
    print('The most popular start station:', popular_start_station )

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().index[0]
    print('The most popular end station: ', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_start_end = df.groupby(['Start Station'])['End Station'].value_counts().sort_values(ascending = False).index[0]
    print('The most popular combination:\n Start station :{}  End station:{} '.format(*popular_start_end))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {} sec'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean of travel time: {} sec'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    #cities which have 'Gender' and 'Birth Year' column in csv
    gender_birth_csv = ['chicago', 'new york city']

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].unique()
    print('User types counts: ',np.size(user_type))

    if city in gender_birth_csv:

        # Display counts of gender
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].sort_values().iloc[0]
        recent_year = df['Birth Year'].sort_values(ascending=False).iloc[0]
        common_year = df['Birth Year'].value_counts().index[0]

        print('Earliest birth year: ', earliest_year)
        print('Recent birth year: ', recent_year)
        print('Common birth year: ', common_year)

    else:
        print('No gender and birth year informations in {}'.format(city))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        #view raw data
        view_raw_data = input('\nWould you like to see raw data? Enter yes or no.\n')
        if view_raw_data.lower() == 'yes':
            while True:
                try:
                    rows = int(input('\nHow many rows?\n'))
                except ValueError:
                    print('Value Error: Input integer value')
                    continue
                else:
                    print(df.head(rows))
                    break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
