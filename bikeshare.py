import time
import pandas as pd
import numpy as np

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York City': 'new_york_city.csv',
             'Washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("\nWhich city would you like to filter by?? New York City, Chicago or Washington??\n").title()
        if city not in ('New York City', 'Chicago', 'Washington'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)

    while True:
        month = input(
            "\nWhich month would you like to filter by?? January, February, March, April, May, June, or type 'All' if "
            "you do not have any preference??\n").title()
        if month not in ('January', 'February', 'March', 'April', 'May', 'June', 'All'):
            print("Sorry, I didn't catch. that. Try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    while True:
        day = input(
            "\nAre you looking for a particular day?? If so, kindly enter the day as follows: Sunday, Monday, "
            "Tuesday, Wednesday, Thursday, Friday, Saturday or type 'All' if you don't have any preference.\n").title()
        if day not in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All'):
            print("Sorry, I didn't catch that. Try again.")
            continue
        else:
            break

    print('-' * 40)
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
    # load data file into dataframe
    df = pd.read_csv(CITY_DATA[city])
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'All':
        # Filter by day of the week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    month_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.month.mode()[0]
    print("Most Common Month: ", month_mode, sep="")

    # display the most common day of week

    weekday_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.day_name().mode()[0]
    print("Most Common Day of the Week: ", weekday_mode, sep="")

    # display the most common start hour

    hour_mode = pd.Series(pd.DatetimeIndex(df['Start Time'])).dt.hour.mode()[0]
    print("Most Common Start Hour: ", hour_mode, sep="")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    ss = df['Start Station']
    start_station = ss.mode()[0]
    print("Most Common Used Start Station: ", start_station, sep="")

    # display most commonly used end station

    end_station = df['Start Station'].mode()[0]
    print("Most Common Used End Station: ", end_station, sep="")

    # display most frequent combination of start station and end station trip

    df["frequent stations"] = df["Start Station"].map(str) + "to" + df["End Station"]
    fs_mode = df["frequent stations"].mode()[0]
    print("Most Frequent Combination Of Start and End Station: ", fs_mode, sep="")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time: ", total_travel_time, sep="")

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time: ", mean_travel_time, sep="")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    subscribers = len(df[df["User Type"] == "Subscriber"])
    customers = len(df[df["User Type"] == "Customer"])
    print('subscribers: ', subscribers, sep="")
    print('customers: ', customers, sep="")

    # Display counts of gender

    try:
        males = len(df[df["Gender"] == "Male"])
        females = len(df[df["Gender"] == "Female"])
    except:
        print('There is no Gender data')
    else:
        print('Males: ', males, sep="")
        print('Females: ', females, sep="")

    # Display earliest, most recent, and most common year of birth

    try:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
    except:
        print('There is no Birth Year data')
    else:
        print('Earliest: ', earliest, sep="")
        print('Most Recent: ', most_recent, sep="")
        print('Most Common: ', most_common, sep="")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    view_data = input('\nWould you like to view 5 rows of individual trip data?? Enter yes or no\n')
    start_loc = 5
    while True:
        print(df.iloc[0:start_loc])
        start_loc += 5
        view_display = input("Do you wish to continue??:").lower()
        if view_display.lower() != 'yes':
            break




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
