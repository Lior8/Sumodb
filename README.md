# Sumodb
This is a python3 program for querying [sumodb's bout query form](http://sumodb.sumogames.de/Query_bout.aspx).

## Content Links
- [Written with](#written-with)
- [Using the package](#using-the-package)
- [Parameters](#parameters)
  - [Basho](#basho-wikipedia)
  - [Day](#day)
  - [Division](#division-wikipedia)
  - [East_side_only](#East_side_only-rikishi1_wins_only-rikishi1_losses_only)
  - [Rikishi1_wins_only](#East_side_only-rikishi1_wins_only-rikishi1_losses_only)
  - [Rikishi1_losses_only](#East_side_only-rikishi1_wins_only-rikishi1_losses_only)
  - [Kimarite](#kimarite-wikipedia)
  - [Rikishi](#rikishi-wikipedia)
    - [Shikona](#shikona-wikipedia)
    - [Include_changes](#include_changes-shikona)
    - [Heya](#heya-wikipedia)
    - [Shusshin](#shusshin-birth-place)
    - [Rank](#rank)
    - [Wins](#wins)
    - [Wins options](#wins-options)
    - [Yusho](#yusho-wikipedia)
    - [Sansho](#sansho-wikipedia)
    - [Division](#division)
    - [Debut](#debut)
- [To-do](#to-do)
- [Contributing](#contributing)

## Written With
- Python 3.7.4
- Pandas 1.0.3
- BeutifulSoup 4.8.2


## Using the package
The program currently does not offer input validation, meaning all validation would be done by sumodb as stated in their [help page](http://sumodb.sumogames.de/Query_bout_help.aspx).

**WARNING:** Do not leave all the parameters empty. This means that you request every bout in the database, which is very costly. Try to have as many parameters as you can when querying the database to not overload it and shorten the processing time.

## Parameters

### Basho ([wikipedia](https://en.wikipedia.org/wiki/Honbasho))
The basho can be written with six digits of year and month (e.g. 200703) or with a **dot** between year and month (e.g. '2007.03'). The notation **'now'** in the Basho parameter means the current (or last) basho. You can also enter specific **years** (or ranges of years) instead of basho. They have to be specified with 4 digits. Years and basho also may be **mixed** (e.g. '2005-2006.07').
```python
query(basho=2007)            # bouts in all bashos of 2007
query(basho='2007.03')       # bouts in basho of March 2007
query(basho='now')           # bouts in the current (or last) basho
query(basho='2007.03-2010')  # bouts in all bashos between March 2007 to the last basho of 2010
query(basho='2010,2012')     # bouts in all bashos of 2010 or 2012
```

### Day
Day also can be specified as ranges and/or comma-separated. Enter 16 for yusho kettei-sen (yusho playoff) bouts.
```python
query(day=15)       # bouts in day 15
query(day='15')     # bouts in day 15
query(day='3-5')    # bouts in days 3 to 5 included
query(basho='3,5')  # bouts in either day 3 or 5
```

### Division ([wikipedia](https://en.wikipedia.org/wiki/Professional_sumo_divisions))
By default, all matching results regardless of division are included. If you don't want that, set the division parameter. Bouts between rikishi of different divisions are always listed as occuring in the higher division.
|Divison  |Abbreviation|Other     |
|---------|------------|----------|
|Mae-zumo  |mz         |maezumo   |
|Jonokuchi |jk         |          |
|Jondian  |jd          |          |
|Sandanme |sd          |          |
|Makushita|ms          |          |
|Juryo    |j           |          |
|Makuuchi |m           |makunouchi|

```python
query(division='m')               # bouts in Makuuchi division
query(division=['Sandanme','jd']) # bouts in Sandanme or Jondian divisions
```

### East_side_only, rikishi1_wins_only, rikishi1_losses_only
The standard output of a search often is giving more results than desired, especially you will often see the same bout two times, just with rikishi switching sides. If you want to limit those results to only one bout you can set one of these parameter to True to determine the condition for the selection.
```python
query(east_side_only=True)       # bouts where the east rikishi wins
query(rikishi1_wins_only=True)   # bouts where rikishi1 wins
query(rikishi1_losses_only=True) # bouts where rikishi1 loses
```

### Kimarite ([wikipedia](https://en.wikipedia.org/wiki/Kimarite))
You can restrict the results by selecting a kimarite from the kimarite enum. 
```python
query(kimarite=Kimarite.OSHIDASHI) # bouts won by oshidashi
query(kimarite=Kimarite.YORIKIRI)  # bouts won by yorikiri
```

### Rikishi ([wikipedia](https://en.wikipedia.org/wiki/Rikishi))
The parameters rikishi1 and rikishi2 represent dictionaries of parameters about the rikishi. These are the parameters:
#### Shikona ([wikipedia](https://en.wikipedia.org/wiki/Shikona))
A rikishi's shikona. This parameter is **case-sensitive**.  
You can also use wildcards * and ?, where * means match anything, and ? means match exactly one character. The whole pattern has to match.  
You can enter more than one shikona at the time, separate them with a comma.
```python
# bouts where rikishi1's shikona is Hakuho
query(rikishi1={'shikona': 'Hakuho'})
# bouts where rikishi2's shikona is 4 letters and ends with an O.
query(rikishi2={'shikona': '???o'})
# bouts where rikishi1's shikona starts with Koto, and rikishi2's shikona is either Hakuho or Tochinoshin
query(rikishi1={'shikona':'Koto*'}, rikishi2={'shikona':'Hakuho,Tochinoshin'}
```


#### Include_changes (shikona)
Include changes enables you to include results under a different shikona – the only condition here is that the searched shikona must have been used at some time in his career.  
Example: writing **Takamisakari** and making include_changes True will also find his results under his former shikona **Kato**.
```python
# bouts where rikishi1's shikona was Takamisakari at some point in his career
query(rikishi1={'shikona':'Takamisakari','include changes':True})
```

#### Heya ([wikipedia](https://en.wikipedia.org/wiki/Heya_(sumo)))
You can restrict rikishi to a certain heya by setting the heya to one of the values in the Heya enum.
```python
query(rikishi1={'heya':Heya.NARUTO}) # bouts where rikishi1's heya was Naruto
```

#### Shusshin (birth-place)
You can restrict rikishi to a certain birth=place by setting the shusshin to one of the values in the Shusshin enum.  
Note that several of the Japanese shusshin are historic and not in usage anymore since 1946.
```python
query(rikishi={'shusshin':Shusshin.TOKYO})           # bouts where rikishi1 is from Tokyo
query(rikishi1={'shusshin':Shusshin.ALL_JAPANESE})   # bouts where rikishi1 is japanese
query(rikishi1={'shusshin':Shusshin.ALL_FOREIGNERS}) # bouts where rikishi1 is a foreigner
```

#### Rank
Rank can be specified in a number of ways, please refer to [sumodb's help page](http://sumodb.sumogames.de/Query_bout_help.aspx) for more information.
```python
query(rikishi1={'rank': 'M10e'})     # bouts where rikishi1's rank was M10e
query(rikishi1={'rank': 'M23-M10'})  # bouts where rikishi1's rank was M10 or lower
query(rikishi1={'rank': ['M','J']})      # bouts where rikishi1's rank was Maegashira or Juryo
```

#### Wins
Wins can be specified as ranges and/or comma-separated, just like rank.
```python
# bouts where rikishi1 was at 11 wins after the bout (as it is the default option)
query(rikishi1={'wins':11}
# bouts where rikishi1 was at 11-13 or 15 wins after the bout
query(rikishi1={'wins':'11-13,15'}
```

#### Wins options
Change the meaning for the wins parameter with the Wins enum.
```python
query(rikishi1={'wins':8,'wins options':Wins.BEFORE_BOUT} # bouts where rikishi1 had 8 wins before bout
query(rikishi1={'wins':8,'wins options':Wins.BASHO_TOTAL} # bouts where rikishi1 had 8 wins in the basho
```

#### Yusho ([wikipedia](https://en.wikipedia.org/wiki/Y%C5%ABsh%C5%8D))
Restrict search to by yusho options with the Yusho enum.
```python
# bouts where rikishi1 was not the winner or runner-up (or in playoffs) in that basho
query(rikishi1={'yusho': Yusho.OTHER})
# bouts where rikishi1 was in yusho-playoff at that basho or won it
query(rikishi1={'yusho': [Yusho.YUSHO,Yusho.YUSHO_PLAYOFF]})
```

#### Sansho ([wikipedia](https://en.wikipedia.org/wiki/Sansh%C5%8D_(sumo)))
Restrict search to bouts of rikishi who got certain sansho (or none) with the Sansho enum.
- Shukun-sho = Outstanding Performance Prize
- Kanto-sho = Fighting Spirit Prize
- Gino-sho = Technique Prize
```python
# bouts where rikishi1 won the Kanto-sho
query(rikishi1={'sansho':Sansho.KANTO_SHO})
# bouts where rikishi1 won the Gino-sho or no sansho
query(rikishi1={'sansho':[Sansho.GINO_SHO,Sansho.NO_SANSHO]})
```

#### Division
By default, all results are included. If you want to restrict to inter-divisional bouts, set the parameter to Division.FROM_LOWER. Setting the parameter to Division.SAME_AS_BOUT for both rikishi will restrict the results to intra-divisional bouts.
```python
# inter-divisional bouts where rikishi1 rank is lower than the bout's division.
query(rikishi1={'division':Division.FROM_LOWER})
# intra-divisional bouts where both rikishis' rank is the same of the bout's division.
query(rikishi1={'division':Division.SAME_AS_BOUT},rikishi2={'division':Division.SAME_AS_BOUT})
```

#### Debut
With the Debut parameter you can search for first appearances at a certain position on the banzuke.
- **Division** finds division debuts (first time in makuuchi, juryo or one of the lower divisions).
- **Rank** finds rikishi who are on a new career high rank in that basho.
```python
# bouts where Tochinoshin made a division debut
query(rikishi1={'shikona':'Tochinoshin','debut': Debut.DIVISION}
# bouts where Tochinoshin made a rank debut
query(rikishi1={'shikona':'Tochinoshin','debut': Debut.DIVISION}
```

## To-do
- Add tests
- Add support for shikona list
- Add support for rikishi wins list
- Add support for str kimarite, heya, shusshin
- Add support for mixed lists
- Add support for 'X or lower/higher' for all divisions
- Add support for normal searching of sanyaku
- Test old bouts or ones with missing data
- Add parameter validation
- Add json support
- Add support for string in heya, shussin, and kimarite
- Add support for complex queries which sumodb does not support (multi-heya for example, or AND between the sanshos)

## Contributing
Just open an issue in the repository and we'll get in touch.
