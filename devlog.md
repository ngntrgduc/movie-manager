2025-12-11
- pytest docs is bad, bro
- StringIO provide: no disk access . Much faster than TemporaryFile in tempfile
- use scope='module' for pytest fixture for file-only level
- add testing with pytest

2025-12-10
- use uv sync --dev (or uv sync) to install runtime and dev dependencies (like pytest)
  - uv sync --no-dev to not include dev group
- uv add --dev pytest to add pytest for testing in a group dev
- testing with pytest

2025-12-04
- add fetch_rows_count, refactor code

2025-12-03
- Add --note for update command just for updating note. Add just_note for prompt_update to do this
- Add back --stats flag for filter command
  - using bare python, simple Counter from functool instead of SQL

2025-12-02
- Add --clean flag for filter option to hide column filtered, like hide country when -c k is specified. (change in print_rows, with hide_columns)
  
2025-12-01
- for personal recsys, sentiment analysis on note does not need to worry about bias and spam note

2025-11-30
- Use absolute import instead of relative import for streamlit_helper.py
- *soft-coded: changable at runtime*
- Dynamic get types, statuses, countries for add command (prompt_add_movie). Change for prompt_update_movie too
  - create utils/constants.py then store in it
  - Should fetch countries from db because both web app and cli allow user to add new country, cannot hard coding it
- Refactor: move hard-coded statuses, types, countries to utils/constants.py

2025-11-29
- ~~switching to 5 star with half-point instead of 10~~
  - affect current logic: need to hand 0.5 point. Click.prompt does not handle this
  - easier to interpret
  - 5-point rating is just suitable for star-rating UI

2025-11-28
- check if it safe to delete apply_filter and print_df
  - remove apply_filter and print_df
- remove rich.print in run_sql
- Benchmark if manually hiding column for print_rows is faster than select all column except rating and watched_date if status = 'waiting' using SQL, difference is negligible
- using: SELECT id, name, year, status, type, country, genres, note FROM movie_detail when status is waiting considered hard-coded, though it has faster runtime (negligible), but lose some flexibility compare to manually hide columns. Also harder to maintain if the schema change, more consistent result of SELECT *. Let display layer handle this instead of get_filter_query
- Rethinking of remove empty column (just for specific use case: when filter with status = waiting, user often use --note when status=waiting, so hide rating and watched_date will have more space for note column)
  - ~~hide rating and watched_date only when both status = 'waiting' and --note is used~~ -> Cluttered for not using --note
- run_sql should not print the result, return rows and column names instead is better
- using walrus operator for assign value := row[i] when adding rows speed up runtime (less index access)
- fix stats command show total by adding print_total to print_rows
- move get_connection from utils/movie.py to utils/db.py

2025-11-27
- using sql for filter command + print_rows. In the past, tested for SQL but with print_df, maybe the speed is not improved (often worse) compare to the pandas original, but now, test with sql + print_rows is soo much faster compare to pandas (print_df)
  - Use sql to get contry, status, type for resolve_choice, less hard coding, more flexible (country remember to IS NOT NULL)
- sorting in filter command never have wrong order
- using print_rows remove the auto hiding empty column mechanism (this is in the print_df function)
- Update --sort help message in filter command
- ',' || genres || ',' is negligible on 10K rows + 10 genres
- utils/file.py for optimize command
- if note_cotains is used, show note eventually: note = True
- add full year support for watched_date filtering in filter command 

2025-11-25 - 2025-11-26
- add optimize command which use VACUUM
  - VACUUM completed. Size reduced from 76.0 KB to 72.0 KB (4.0 KB, 5.3% reduction). (for 299 movies)
- search command for name or note field, using sql
  - search both note and name and show note when --note is passed will cause conflict with other --note option in other commands, inconsistent UX
  -> just enable search for note and show note when --note is passed. Also, this feel more natural
  - search command more intuitive than filter command for searching by text.
- implement recent command, with parameterized (placeholder) script, placed in a folder and hide it from sql command
  - using run_sql for reusability
- implement latest command
- using pathlib iterdir is faster than pahtlib glob, because it doesn't parse pattern for file names
- Create a function to format float to int when using print_rows (all in run_sql)
- create utils/sql.py, move all utilities of sql command to that
- parameters for fetch_rows and run_sql
- rich.console cannot reduce width when updating note

2025-11-24
- fix showing genres updated for update command because of differ format (list, but the old_format is string)
- Fix cannot sort date in sql command
  - ~~Change all to str first, then let it sort~~ -> cannot enable lexicographic order
- tuple sorting (**schwartzian transform**): Tuples give us a layered sorting mechanism
  - old method leads to string-vs-float comparisons -> causing TypeError
  - use when sorting mixed-type, multiple criteria

2025-11-22 - 2025-11-23
- improve stats command, by reading some of sql files
  - add -v/--verbose for extended statistics
- print_rows instead of print_df (using pandas), faster runtime
- refactor stats command

2025-11-20
- staring recsys
- Why not TF-IDF? TF-IDF downweights words that appear frequently (like "Action"). In movie recommendations, if you love "Action", you want that word to carry heavy weight.
- Sentiment analysis
  - The "Implicit Rating" Fix: If a user watches a movie but doesn't rate it, the system might assume they liked it. Sentiment analysis reads their review/note. If they wrote "Waste of time," the system overrides the "watch" signal and treats it as a thumbs down.

2025-11-19
- Fix cannot sort watched_percent in sql genres
  - maybe remove the '%' for percent, also maybe convert to float
    - using key with lambda for pandas apply
    - use df[matched_column].astype(str).str.contains('%').any() instead of checking 'genres' in the column name or not -> more reliability, still work if the column name doesn't has 'percent'
  - resolve_choice maybe not suitable for sql command (which may contain columns with same initials) -> fuzzy matching
- '-', '+' order when sorting for sql command

2025-11-18
- Maybe convert list genres and string genres back and forth is deprecated, because in the past, needed to convert it to string in order to write to csv file. Now sqlite require list of genres instead of string of genres, so maybe it safe to remove it
- remove the string representation and pass the list of genres directly in utils/movie.py
- update to github, merge sqlite
  - use personal database with removed notes data
- add --sort for sql command
- set(genres) shouldn't be converted to set directly because the cost is negligible, and often slower
- touching some string similarity metric
  - levenshtein distance
  - hamming distance
- know about difflib standard lib in python
- pathlib.Path.with_stem only work if only the path has a suffix
  - https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.with_stem
- prefix match and fuzzy match for sql filename in sql command
- Add '-s' for sql command
- Cannot use custom click class to make order in --sort in sql commannd be optional, nargs=2 always require 2 values
- refactor: use genre lists instead of comma-separated strings to reduce redundancy
- rename utils/data to utils/streamlit_helpers
- Allow more sort in filter command
  - sort order can be pre-defined with order:
    - asc for name, id (default), year, watched_date, status, type, country
    - desc for rating
    - no need sorting for genres, note
    -> so just need to check for 'rating'

2025-11-17
- Rename add_movie.py and edit_movie.py with number before name, to manually handle order, using git mv
- Add Refresh button in Data and Edit page to refresh dataframe, better UX
- Prepare_save_df function in streamlit web ui deprecated. because this function convert list of genres to string of genres separated by commas to be compatible with pandas dataframe saving to csv -> no need for literal_eval
- No need st.rerun on Reload button
  - when adding movie, without rerun, without reload button, then after adding new movie, it go to the top of data and the newly typed movie is disappear
  - when adding movie, without rerun, with reload button, then after adding new movie, it work, doesn't glitch
  - add, update, reload, then go to Data page, no glitch
  - add, update, then go to data page -> no glitch
  - add, update, then go to data page, go back to Edit page, add, update -> no glitch
  - add, update, add -> glitch
  - With rerun() when pressing Refresh button
    - add, update, refresh, add, update -> no error
    - add, update, refresh, go to data page -> no glitch on data page but a short glitch (due to re-render when refresh) after refresh on Edit page
  - add in add page, then go to data, doesn't appear -> need refresh button

- For genre filtering in filter command in CLI, first, match the entire genre name, if no result, implement fuzzy matching, if not have, then return No Data.
  - implement genres fuzzy matching for filter command, and prevent printing all data after filtering
- using `in` operator for fuzzy match genres instead of `startswith`, provide better UX, more forgiving, slower a bit but the cost is negligible, just trade-off between UX and optimization
- ~mask will produce a new pandas Series, not performant as mask[:] = False
- multiple commit is slow
- complete Edit page to work with SQLite

2025-11-16
- pdate twinking watermelon, boyhood, lady bird, 2521 genre has coming of age genre
- bug in add page when tabbing
  - The problem was: session_state resets → widgets recreated → DOM nodes replaced → focus lost
  -> Do NOT reset session state inside the same run as widget creation.
  - toast + reset_form doesn't cause DOM reordering
  - toast + reset_form + clear cache cause glitch
    - at first, after press enter on add button, the DOM order is reset, then if tab, it focus on name, but then if tab again, it cause glitch and then focus back to name field instead of year field
- complete add_movie.py, remove load_data_with_cache and clear cache to avoid glitch in Add page because of DOM order changed by re-run
  - Automatic cache clearing on add is convenient, but in Streamlit, any automatic clearing can cause widget remounts and focus issue -> Bad UX
- change layout add page, more compact

2025-11-15
- Improve csv_to_sqlite flow, add file not found handle
  - Delete the file is more efficient compare to droping the tables. But deleting must ensure that there are no working connection operator
- sqlite + streamlit
  - app.py cannot create connection then pass to other pages, so maybe create connection in each page
  - For cache function in utils/data.py, only used for streamlit runtime, will show warning if some file use it not in streamlit runtime, so the best way is to have load_data in another file, then in utils/data.py, import that function, this make **utils/data.py as a cache loader version for another function**
- streamlit sql connection need sqlalchemy to work
  - better to manually handle the connection instead of using streamlit connection
- rewrite prepare csv file (removed note field)
- connection to sqlite database is closed automatically by the OS when the program end, both for CLI app and streamlit web app
- refresh the page when changing the content in cache_resource or cache_data
  - sqlite connection is not thread-safe, and streamlit is multi-threaded
  - Opening a SQLite connection is extremely cheap. Caching it gives no performance benefit
  - sqlite.connect create a connection tied to current thread. If another thread touch it -> crash
  - When using st.cache_resource, the connection gets reused across threads
  -> caching the data, not the connection
  - st.cache_resource is great for: ML models, Heavy objects, API clients, Preloaded assets. Not designed for database connection
  -> should create connection separatedly for each page, each operation -> no sqlite lock issue
  - cache_resource only used for sever-style application, never with sqlite

2025-11-14
- must enable PRAGMA foreign_keys = ON; to make delete cascade on movie_genre table, recognize this today because newly added movie suddenly have 'test' genre (from the old deleted movie links in movie_genre)
  - Solution: enable PRAGMA foreign_keys = ON; everytime we connect to the database
  - PRAGMA foreign_keys = ON is NOT costly.
  - official docs: "Foreign key constraints are disabled by default (for backwards compatibility), so must be enabled separately for each database connection." source: https://sqlite.org/foreignkeys.html#fk_enable
- Keep the web app using pandas filtering, if use sql, it will run the sql query whenever the filter change
  - streamlit work with pandas better than sqlite
  - build a where_clause in web app is complex, and slower compare to pandas filtering (old method)
- For stats command for filtered data, handling filters for SQL method help in filtering in print_stats function using SQL (1 funtionality for 2 functions)
  - but the speed is slower than pandas filtering
- the delete method work even there is a connection to sqlite database, as long as the connection doesn't do anything
- no need to do watched_date gap for this data, forgot to include month-date in 2023
- Ask gpt to generate question and complex sql query to answer that question, given schema.sql, and sample values
- Fix prompt_update_movie: handle None and string for click compatible
  - click receive empty string, not None value (default is existing_movie, which contain None value -> bug)
- backup, restore command work in sqlite database instead of csv
  - when backup in csv, need to write entire file to csv
    - when restore, need to perform csv_to_sqlite
  - when backup in sqlite, just need to use .backup
    - when restore, just need to copy file
  - only need to close CON on restoring if the CON is being used during restore
  - restore command need update_csv

2025-11-13
- using pandas to handle nan value is unnecessary in `add_movie` function when using in CLI app, but for csv_to_sqlite script, must handle nan value manually
  - Handle NaN values in CSV import and simplify CLI add_movie, remove importing pandas in add_movie to speed up CLI app
- default CLI will have id column
- research on sql command
- add sql command
  - write 16 sql script: country, genres, goodwatch, korea, lastmonth, lastyear, latest, rating, recent, thismonth, thisyear, watched, watchedgenres, year
- still use pandas approach for filtering purpose later on, for modularity (already have print_df), instead of using rich.Table directly
- sql command idea
  - ~~Find the longest “watch gap” (difference between two watched dates).~~ -> Required full date format for watched_date
- SUBSTR is faster strftime because it just string slice, instead of date parsing, date validation
  - also, work great on year-only data (2023), strftime doesn't work for year-only data

2025-11-12
- something like handle_none(click.prompt(...)) is very bad practice, increase cognitive load, handle None manually please
- explicit setting row_factory instead of creating function for code readability
- fix sqlite none value compatibility
- add get command
- move input mechanism to new file
- change in README note section: `rich.Table` doesn't handle link well, use `get` command instead
- add update command
  - the update command cannot help user clear the field value, it just let user edit it
- Compare performance of
  - SELECT * FROM movie_detail WHERE status != 'waiting' -> bad if no index
  - SELECT * FROM movie_detail WHERE status = 'completed' OR status = 'dropped'
  - SELECT * FROM movie_detail WHERE status = 'completed' UNION SELECT * FROM movie_detail WHERE status = 'dropped'
  - SELECT * FROM movie_detail WHERE status IN ('completed', 'dropped');
    - if there're no indexes, all have same performance, but when having indexes, OR/IN method work best, while != perform a full scan. UNION perform worse because it scan the table twice

2025-11-11
- Implement `get` command for getting movie information solve unclickable link for filter command (with rich Table display)
- cannot use RETURNING clause for update command because: "The RETURNING clause does not report any additional database changes caused by foreign key constraints or triggers." -> cannot get update from movie_detail
  - just printing dict contain changed value -> better performance, but bad UX
  - use get_movie instead of RETURNING -> better UX, and cost is negligible with print dict, also confirm that the updated data is correct
    - ~~coloring updated field~~ -> too much works, make code more complex and harder to matain
- Doesn't need RETURNING for 
  - DELETE because has get_movie function
  - INSERT because already see the input in CLI
- py cli sql genres: name, COUNT(*), id, AVG(rating)

2025-11-10
- should the project need testing?
  - use :memory: when testing for sqlite db, CRUD
  - just forcus on csv_to_sqlite.py and CRUD db operation logic: add, delete, update (because both web app and CLI use this functionality)
- if not note is faster than if note == ''

2025-11-09
- When Delete a movie, then insert a new movie right after, it will **use old deleted movie id**
  - When delete a movie (not latest), then next adding movie will not have the id of deleted movie
- use CURRENT_DATE syntax in sql (ANSI standard) to refer to get today date, portable with other relational database, instead of using DATE('now') or DATE()
- Add delete command
- Refactor: Move CLI utilities into utils/cli.py

2025-11-08
- realize that the auto remove empty columns doesn't work any more, for example: py cli.py filter -s w will still show watched_date column, not hide it
  - the problem is when adding movies, the watched_date column recieved '' (empty string) values, so it treated differently from the old migrated data from csv to sqlite (treated as None/NULL)
  - pd.read_sql_query treat '' different from None/NULL value, and will not convert '' to NaN, it return whatever it stored
  - sqlite treat None in Python as NULL in sqlite, and treat '' as TEXT, not NULL
    source: https://docs.python.org/3/library/sqlite3.html#sqlite-and-python-types
- because using pandas.read_sql_query to read data from sqlite, so there no penalty to use it in other place, no need to avoid pandas as much as possible

2025-11-07
- Added status message when adding movie
  - No need to Make status message for update, delete command, it fast
- add `stats` command for CLI
- fix `timing` util (using wraps from functool), work well with Click now
- Keep the connection CON to the database globally, no need for lazy create it in command that interact with database, that would over-engineered
- ~~Auto commit mode for add, update, delete~~ -> Can because it take cursor, not con, so cannot access to con.commit()
- Using sqlite directly to get movie information instead of pandas. Sacrifices beauty format for speed
  - also, dataframe when printing to console cannot keep the full content, while rich.print can do this
  - also, the rich table format for dataframe make reading content harder, especially when text in note column is long, while rich.print handle this so well with tuple printing
- understand sqlite3 row factory: format the result of cursor, sqlite3.Row is very optimized (C-level) for tuple with key accessing like dict
  - **sqlite3.Row is very optimized (C-level), acts as a Mapping object, so we can directly use dict() on it instead of dictionary comprehension**
  - cannot use dict_factory because it will break pd.read_sql_query, use dict() directly on sqlite3.Row instead
- python `is, is not` operator (IS_OP) is faster than equality operator, use this for checking None (class object), work especially well with fetch in sqlite (return None if there is no value)
- no need to use console.print(width=80) to reduce width of dict content in delete command, because we just need to print it for deletion confirmation, no need to reduce eye strain

2025-11-06
- keep `from utils.movie import add_movie` loaded later in `add` command, for better UX

2025-11-05
- for update_movie function, it doesn't handle `genres` field yet, beucase movie table doesn't have `genres` field, must handle manually
`UPDATE movie SET genres = ? WHERE id = ? [['romance', 'comedy', 'test'], 'movie_id']` -> formated as list of genres
- adding movie to database + write to csv took: Took 0.7199s
- adding movie to csv (old method) took: Took 0.6454s
- loading dataframe with_index=True and then write csv without index is faster than load dataframe with column id then drop it, then write to csv because the latter load all column, more memory usage, extra `drop` operation call
- Start commiting to sqlite branch
- switch to sqlite:
  - CLI: add command

2025-11-04
- the `date` field in column config appear when edit data in Edit page is mathed with `watched_date` in the schema
- CLI edit having old data as default
- set index_col='id' when running pd.read_sql_query will set index to 'id', easier to access for streamlit UI, and when select data, just using df.iloc[row].to_dict(), this doesn't contain id column, ready to pass to add_movie function right away. If not setting index='id', we will manually handle id column
- create `sqlite` branch, start migrate to sqlite

2025-11-03
- pd.read_sql_query is faster than pd.read_csv
  - sql run in 0.006, when csv run in 0.55, at 248 movies
- Delete using sql is faster than delete using pandas to overwrite entire csv file
- after CRUD ops, in the end we must read it, and sql always win in loading speed compare to csv pandas
- pd.read_sql_query give same type of data column when using pd.read_csv
- using sqlite help CLI app can Edit/Delete movies through id (by include `id` field in movie_detail and in rich Table when printing)
- multiline note work in CSV but not beautiful, after using SQLite, CSV file will act as instance/copied version of data for Web app and Power BI dashboard, adding changes to CSV file don't change anything
  - make this switch when implemented all CRUD operations
- for switching to sqlite, Edit page won't need to store edited df in variable edited_df -> reduce memory, only work with session_state instead of access the entire edited df, with dict structure:
  - `{'edited_rows': {}, 'added_rows': [], 'deleted_rows': []}`, source: https://docs.streamlit.io/develop/concepts/design/dataframes#access-edited-data
- the streamlit dataframe current display position, not the DataFrame index, so it hard to get movie id when on streamlit UI

2025-11-02
- release v0.1.3
- cli with sqlite, streamlit with pandas is not sync well, because streamlit work on pandas dataframe, edit on dataframe cannot convert to sqlite the easy way. The best optimized way is handle in sqlite and then convert to csv for web ui, cli, and dasboard
  - but this will lose instant edit on csv, making edit/update in sqlite seem a bit complicated
- if filtering using sqlite in CLI, then must use movie_detail view instead of movie table, regardless filter options
- no need for data versioning
- Database partitioning for watched-year -> overkill, also not fully support in SQLite

2025-11-01
- Add `restore` command
  - shutil.copy is slower than shutil.copyfile because it copy meta data

2025-10-31
- some ideas to switch to sqlite
  - in csv format, when editing, it must write entire updated content to file, when in database, it just has to write the change to specific movie, not rewriting entire database -> more performant
- for stats command, consider switching to sqlite because it avoid reading all data like current method (using pandas to read entire csv file then extract information for statistics)
  - consider query on movie table instead of movie_detail view
  - note that switch to sqlite will break stats functionality for filtered data
    - filtered data as movie_detail, so it still need to query on movie_detail, then query on movie table will break when apply to filtered data
      - ~~using CTE for filtered data~~ -> CTE is limited to execution scope
      -> Hybrid approach: If no filters were used, run stats using sql (fast). If filters were applied, use pandas value_counts() on filtered_df (old method)
- no need for Triggers now, this add to much complexity, also not really needed

2025-10-30
- try out DBeaver, great
- complete basic csv_to_sqlite and sqlite_to_csv in self-learn-db project
- public TODO.md

2025-10-28
- try out sqlite, so fast :)

2025-10-26
- Research on making the switch to **parquet** file format
  - parquet shine on large dataset, with small csv data file (<20mb), parquet is overkill
- Complete criteria

2025-10-24
- research on flat file vs database:
  - flat files need to write the entire file just to update a single record -> very inefficient

2025-10-19
- Ignore tracked data.csv and dashboard.pbix using `git update-index --assume-unchanged <file>`
  - Then using `--skip-worktree` instead for safe branch switching: `git update-index --skip-worktree .\data\data.csv .\dashboard.pbix`
  - Untracked `backup.csv`

2025-10-17
Ask chatGPT -> Using hybrid approach, devided in 3 phase:
- Phase 1: Keep CSV as main storage, add SQLite “shadow” DB
- Phase 2: Gradually migrate the app to read from SQLite
  - filter via SQL or still use Pandas filtering on the result DataFrame.
  - No need to fully replace pandas logic yet
  - For CLI commands, test inserting/deleting rows via SQL, but still export to CSV afterward for Power BI
- Phase 3: Full SQLite adoption (optional)
  - Move CRUD logic fully into SQL.
  - Remove CSV from main workflow.
  - Power BI connects either via ODBC or via periodic exported CSV snapshots.

2025-10-03
- Tried to use click.DateTime for `year` field, but unsuccessful
  - The code look shorter, but reduce readability when dealing with no year, use datetime.min and before write to data file, check if the year is equal 1 or not
    - ```
      # quick and strict input, doesn't need to handle None year
      # year = click.prompt('Year', type=click.DateTime(['%Y'])).year
      ```
  - also, a bit overkill for just simple year inputting
- value_proc execute right after user press Enter for the input, so the type validation specified not handle the input yet
- using repr format for string representation instead of explicit quotes

2025-09-30
- Add CLI
- Know how to add optional dependencies when working with uv

2025-09-28
- Add dependencies using uv
- Remove FutureWarning of pandas.concat when concatenate with empty or all-NA entries
- Take a look at st.fragment but a bit over-engineering for now
- Add cache for loading data, getting options, and loading column config
- Add demo data and Power BI dashboard
  - Fix data loading when column not is all-NA
- Public repo GitHub

2025-09-27
- Refactor code
- Change mask-based filtering, more efficiently
- Change to subset operation when filtering genres for faster performance
- Integrated options loading in load_data function, more efficient for later caching

2025-09-26
- Change `Add` page layout: The left container is optimized for quickly adding movie info via `Tab` key, and the right container is for detail added after watching
- Switched to whole numbers (1–10) for ratings, removing half-point steps.  
  This simplifies input (reduces cognitive load), keeps Power BI charts cleaner (fewer bins), aligns with common standards like IMDb, and reflects the fact that a 10-point scale is just 5-point scale with half-point steps
- Refactor code for `Add` page
- Add write_data function

2025-09-25
- Initial commit for basic working web app