import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Compatibility fix for deprecated np.float in newer NumPy versions
if not hasattr(np, 'float'):
    np.float = float

# Import data
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)

# Clean data: remove top and bottom 2.5% (strict inequalities, overwrite df)
df = df[(df['value'] > df['value'].quantile(0.025)) & (df['value'] < df['value'].quantile(0.975))]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df['value'], color='red', linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    fig.savefig('line_plot.png')
    plt.close()
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month

    # Group by year and month, then calculate mean
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()

    # Create month names and ensure proper ordering
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df_grouped['month'] = df_grouped['month'].apply(lambda x: month_names[x-1])
    df_grouped['month'] = pd.Categorical(df_grouped['month'], categories=month_names, ordered=True)

    # Pivot the data
    df_pivot = df_grouped.pivot(index='year', columns='month', values='value')

    # Create the plot
    fig = df_pivot.plot(kind='bar', figsize=(12, 8)).get_figure()
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')
    plt.tight_layout()
    fig.savefig('bar_plot.png')
    plt.close()
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

    # Year-wise box plot
    sns.boxplot(x='year', y='value', data=df_box, ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # Month-wise box plot
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x='month', y='value', data=df_box, order=month_order, ax=ax2)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    plt.tight_layout()
    fig.savefig('box_plot.png')
    plt.close()
    return fig