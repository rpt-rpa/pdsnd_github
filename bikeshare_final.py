import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
    while city not in ('chicago', 'new york city', 'washington'):
        print("Please enter a valid city name from the list.\n")
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Which month - January, February, March, April, May, or June? You may also type \"all\".\n").lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june','all'):
        print("Please enter a valid month from the options listed.\n")
        month = input("Which month - January, February, March, April, May, or June? You may also type \"all\".\n").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? You may also type \"all\".\n").lower()
    while day not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday', 'all'):
        print('Please enter a valid day of the week as listed.\n')
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? You may also type \"all\".\n").lower()


    print('-'*40)
    print('You selected\n city: {}\n month: {}\n day: {}\n'.format(city, month, day))
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

    # convert 'Start Time' column into datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week into new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day if applicable
    if day != 'all':
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = days.index(day) + 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    start_time = time.time()

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    common_month = df['month'].mode()[0]
    print('\nMost Common Month:', common_month)

    # display the most common day of week
    df['day_of_week'] = df['Start Time'].dt.weekday
    common_day = df['day_of_week'].mode()[0]
    print('\nMost Common Day of the Week:', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('\nMost Common Start Hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('\nThe most commonly used start station is: ', common_start)

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('\nThe most commonly used end station is: ', common_end)

    # display most frequent combination of start station and end station trip
    common_start_end = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('\nThe most popular combination of start station and end station trip are: ', common_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print ('\nThe total travel time is: ', total_travel)

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print ('\nThe mean travel time is: ', mean_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df.groupby('User Type').size()

    print('\nThe count for different user types is: ', user_type)

    # Display counts of gender
    if 'Gender' in df.columns:

        counts_of_gender = df.groupby('Gender').size()
        print('\nThe count of gender is: ', counts_of_gender)

    else:
        print('\nThis city does not have Gender data.')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        df['Birth Year'] = pd.to_datetime(df['Birth Year'])
        least_recent_date = df['Birth Year'].min()
        recent_date = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print('\nThe least recent date of Birth is: ', least_recent_date)
        print('\nThe most recent date of Birth is: ', recent_date)
        print('\nThe most common date of Birth is: ', common_year)

    else:
        print('\nThis city does not have Birth Year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays contents of the CSV file as requested by the user."""

    start_loc = 0
    end_loc = 5

    display_raw = input("Would you like to see five lines of raw data? Type \'yes\' or \'no\'.\n").lower()
    # Display 5 rows of data at a time based on user input
    if display_raw == 'yes':
        while end_loc <= df.shape[0] - 1:

            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5

            end_display = input("Would you like to see five more lines of raw data? Type \'yes\' or \'no\'.\n").lower()
            if end_display == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)
        # Asks user to restart or terminate
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
