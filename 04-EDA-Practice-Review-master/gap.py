def avg_gdp_in_decade(country, continent, year):
    ''' 
    this function takes in a country, continent, and year.
    it uses continent in order to format the path to a gapminder csv file, which is read in as a DF
    it uses the country to boolean index the DF and the year to calculate the average GDP in that decade.
    '''
    
    df = pandas.read_csv('data/gap_data/gapminder_gdp_'+continent+'.csv',delimiter=',',index_col=0)
    country_rec = df.loc[country]
    gdp_decade = 'gdpPercap_' + str(year // 10)
    avg = (country_rec.loc[gdp_decade + '2'] + country_rec.loc[gdp_decade + '7']) / 2
    
    return avg