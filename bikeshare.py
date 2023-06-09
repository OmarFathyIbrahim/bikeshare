import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#def get_filters():
    
"""
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
"""

def check_input(userinp, type_inp):
    while True:
        s = str(input(userinp)).lower()
        try:
            if s in ['chicago', 'new york city', 'washington'] and type_inp == 'city':
                break

            elif s in ['all', 'january', 'february', 'march', 'april', 'may', 'june'] and type_inp == 'month':
                break

            elif s in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'] and type_inp == 'day':
                break
            else:
                if type_inp == 'city':
                    print("Sorry, input must be: chicago, new york, washington")
                if type_inp == 'month':
                    print("Sorry, input must be: january, february, march, april, may, june or all")
                if type_inp == 'day':
                    print("Sorry, input must be: sunday, monday, tuesday, wednesday, thursday, friday, saturday or all")
        except valueError:
            print("Sorry, your input is wrong! Please try again")
    return s

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
    city = check_input("Enter the city name would you like to see the data for (chicago, new york city, washington): ",'city')
    # get user input for month (all, january, february, ... , june)
    month = check_input("Which month you need to filter with(all, january, ..., june): ", 'month')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("Which day you need to filter with(all, sunday, monday, ...,saturday): ", 'day')
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    

    # filter by day of week if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Month: ', popular_month)


    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('Top Day Of Week: ', popular_day_of_week)
    
    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour: ', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Start Station: ', popular_start_station)


    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most End Station: ', popular_end_station)


    # display most frequent combination of start station and end station trip
    #Here we can't use mode, instead we will use group.
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is: ', total_travel_time)


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time is: ', mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts().to_frame()
    print('Here are users types:\n', user_types)
    
    # TO DO: Display counts of gender 
    # I used try / except to avoid any difference between cities data 
    try:
        print("Gender is\n", df['Gender'].value_counts())

    #Display earliest, most recent, and most common year of birth
        print('Earliest year of birth is', df['Birth Year'].min())
        print('Most recent of birth is', df['Birth Year'].max())
        print('Most common year of birth is', df['Birth Year'].mode()[0])    
        
    except:
        print('No filter with gender allowed in Washington city!')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#view raw data to user
def show_row_data(df):
    row=0
    while True:
        view_raw_data = input("Would you like to see the raw data? for 'Yes' enter 'Y' and for 'No' enter 'N'.\n").lower()
        #row = 0
        if view_raw_data == "y":
            print(df.iloc[row : row + 5])
            row += 5
        elif view_raw_data == "n":
            break
        else: #validate user input
            print("Sorry! You entered Wrong Input, Kindly try Again!")     

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
