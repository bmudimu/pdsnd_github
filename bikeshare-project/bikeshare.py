import time
import pandas as pd
import numpy as np

# This file was updated for the git proect 10/12/2019

month_list = ['january', 'february', 'march', 'april', 'may', 'june']
day_list = ['sunday', 'monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

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

        city = input('Enter city to analyze => chicago, new york or washington: ')


        # get user input for month (all, january, february, ... , june)
        print('\nEnter month between january and June to analyze or ')
        month = input('just press Enter to use all months: ')
        if month == "": month = 'all'


        # get user input for day of week (all, monday, tuesday, ... sunday)
        print('\nEnter any day from monday to sunday to analyze or ')
        day = input('just press Enter to use all days: ')
        if day == "": day = 'all'


        print('-'*40)

        filter_prompt = input('\nAre you happy with the following filters: \n City: {} \n Month: {} \n Day: {} \n Enter Yes[Y] or No[N]: '.format(city, month, day))

        if filter_prompt.lower() == 'yes' or filter_prompt.lower() == 'y' or filter_prompt.lower() == '' :
            break

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
    df = pd.read_csv(city.replace(" ", "_").lower()+".csv")
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Hour'] = df['Start Time'].dt.hour
    df['Day'] = df['Start Time'].dt.day
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.weekday_name
    df['Month_name'] = df['Start Time'].dt.month_name()

    if month.lower() in month_list: # If a month filter has been provided
        months = dict(zip(df.Month_name.str.lower(), df.Month))
        month = months[month.lower()]

        df = df[df['Month'] == month]

    if day.lower() in day_list: # If a day filter has been provided
        df = df[df['Day_of_Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    print('-'*60)
    start_time = time.time()

    # display the most common month
    print('\nThe most frequent month of travel is: {}.\n'.format(df['Month_name'].mode()[0]))


    # display the most common day of week
    print('\nThe most frequent day of travel is: {}.\n'.format(df['Day_of_Week'].mode()[0]))


    # display the most common start hour
    print('\nThe most frequent hour of travel is: {}.\n'.format(df['Hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('\nThe most commonly used start station is: {}.\n'.format(df['Start Station'].mode()[0]))


    # display most commonly used end station
    print('\nThe most commonly used end station is: {}.\n'.format(df['End Station'].mode()[0]))


    # display most frequent combination of start station and end station trip
    print('\nThe most commonly used start and end route is: {}.\n'.format(pd.Series(list(zip(df['Start Station'], df['End Station']))).mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nThe total travel time is: {}.\n'.format(sum(df['Trip Duration'])))


    # display mean travel time
    print('\nThe mean travel time is: {}.\n'.format(df['Trip Duration'].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Handle missing columns in the csv files
    if 'Gender' in df.columns:
        gender_count_dict = df['Gender'].value_counts().to_dict() # to pick indvidual values and not print the default value_counts table
        print('\nHere are the counts by gender \n')

        for key in gender_count_dict:
            # Display counts of gender
            print(key.lower() + ': {} \n'.format(gender_count_dict[key]))
    else:
        print('\n' + '-'*20 + ' The selected data set has no Gender infomation ' + '-'*20 + '\n')

    if 'User Type' in df.columns:
        user_count_dict = df['User Type'].value_counts().to_dict() # to pick indvidual values and not print the default value_counts table
        print('\nHere are the User Type counts \n')
        for key in user_count_dict:
            # Display counts of user types
            print(key.lower() + ': {} \n'.format(user_count_dict[key]))
    else:
        print('\n' + '-'*20 + ' The selected data set has no User Type infomation ' + '-'*20 + '\n')

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth: {}.\n Most recent year of birth: {}.\n Most common year of birth: {}.\n'.format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))
    else:
        print('\n' + '-'*20 + ' The selected data set has no Birth Year infomation ' + '-'*20 + '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    # get user input for raw data
    raw_prompt = input('\nWould you like to see 5 rows of raw data? Enter Yes[y] or No[n].\n')
    rows = 5
    if raw_prompt.lower() == 'yes' or raw_prompt.lower() == 'y':
        print('-'*120 )
        print(df.loc[:, 'Start Time':'Hour'].head(rows))
        print('-'*120 )

        raw_prompt = input('Do you want to see 5 more rows? Yes[y] or No[n].\n')
        while raw_prompt.lower() == 'yes' or raw_prompt.lower() == 'y':
            rows += 5
            print('-'*20 + 'Here is {} lines of raw data:'.format(rows) + '-'*20)
            print(df.loc[:, 'Start Time':'Hour'].head(rows))
            raw_prompt = input('Do you want to see 5 more rows? Yes[y] or No[n]. \n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input()
        station_stats(df)
        input()
        trip_duration_stats(df)
        input()
        user_stats(df)
        input()
        display_raw(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
