# csv-to-datatable-converter

#### Problem statement:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
At my work when I do NLP-ML tasks where I need to build a model for multi-class text classification, my training set is usually in csv format with two main columns, where I have product descriptions (text) and their product categories (target classes) respectively, and most of the times the product categories are not accurate enough where some product categories have a lot of irrelevant product descriptions.  

Ex:
ne of the product categories is *Shampoos* category where it should have only shampoo product descriptions. But there could be a lot of hair conditioner product descriptions which are irrelevant to *Shampoos* category.  

So, before training a model, I needed to look through each category descriptions quickly by google searching some portion of them and annotate irrelevant ones as False and download it back into new csv file with annotation. And I did this portable *csv-to-datatable-converter* that gives me desired functionalitiy features to do my trainset checkup.  

#### What project does:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The python script converts columns from csv file into separate html file as table. The main thing the converted html file offers is that you can quickly search and find needed product descriptions by using search fields, annotate each text (e.g. product descriptions) as True/False in separate table column, google search the product descriptions and download as csv file using quick shorcuts.  

#### Usage:  
* a)  
Run in terminal:  
```
python csv_to_html.py -f <file path> -o <out file>  
```
\<file path\> - csv file path you need to convert into html.  
\<out file\> - name for out html file that will be generated. If out file name is not passed, default name will be given which is **filled_template**.    

* b)  
After script is launched, it will start analyzing csv file to get column names and column data types.  
Once analysis is complete, brief columns summary can/will be printed.  
where original column names and their types are shown in 'column names' and 'column types' respectively.  

* c)  
User will be prompted to indicate columns that needs to be included in html file.
And again columns indexes need to be indicated seperated by commas.
or if all columns needs to be included, user can just press ENTER key.  

* d)  
And finally you will get your html file.  


#### Example usage:  

Let's take 10000.csv file in test_csvs folder and generate html file from it. If you run the following in terminal:
```
python csv_to_html.py -f test_csvs/10000.csv -o my_html  
```
you will get the following in terminal:

```
====================================================================================================
FILE DESCRIPTION:
  csv file path:     test_csvs/10000.csv
  csv file:          10000.csv

  Analyzing file ...
    Rows count:      9999

    Column names and types:
	 1    description                    Text
	 2    description_norm_alphanum      Text
	 3    description_norm_alpha         Text
	 4    anno_type                      Text
	 5    month_                         Integer
	 6    source_                        Text
	 7    by_means                       Text

====================================================================================================
INDICATE COLUMNS TO BE INCLUDED:

  Enter column order numbers seperated by comma:  1,5
```
and for demonstration purposes I provided **1** and **5** column indexes meaning that only 1st column *(e.g. description)* and 5th column *(e.g. month_)* needs to be included in html file.

And then you will see the following final summary messages after which **my_html.html** file will be generated inside main **csv-to-datatable-converter** folder:
```
  Following columns selected:
   ['description', 'month_']

Processing data from CSV file ...
	The output html file will be called as [my_html.html]

Processed 9999 rows
Processing took 0.146656 s
```
  
  
As a reference you can find **my_html.html** file is in the example folder. And this is how the **my_html.html** file looks like if you open it in browser:  
![alt text](https://github.com/altayaman/csv-to-datatable-converter/blob/master/example/my_html_image.png)  


#### All features of generated html file:  
* #1  
As the default search filter of datatables are doing only default including-AND search, 4 types of search filters are implemented:  
1 - including-AND search  (searches/shows any string value that contains all search values)  
2 - excluding-AND search  (hides any string value that contains all search values)  
3 - including-OR search   (searches/shows any string value that contains at least one of search values)  
4 - excluding-OR search   (hides any string value that contains at least one of search values)  

* #2  
Table cell values are google-searchable on click on value itself.  

* #3  
Datatable has 'TF Type' column that provides radio buttons for each row where one of two values (True, False) can be selected.  
And 'TF Typeid' column values change according to checked/selected value in 'TF Type' column.  

* #4  
Datatable config was set up so that it does not sort your data when it opens. But data entries can be sorted by clicking on column name.  

* #5  
When you close the table or refresh the page, it will give pop-up warning window so that you do not close/refresh your page.  

* #6  
The whole datatable can be downloaded as csv file where 'TF Type' column is not included purposely as a part of feature.  

* #7  
There is toogle buttons which can hide/unhide corresponding column on click. Every toogle button has corresponding column name it hides/unhides.  

* #8  
Table cells can be navigated using keyboard arrow keys once clicked on any of them.  

* #9  
On space-button click the table cell value is google-searched in own new separate window (not tab).  

* #10  
On E button click the table cell value is google-searched in own new separate window (not tab), but google-search results are extracted in a plain text links format.  
Note: For the E-key functionality to work, it is needed to install CORS plugin in Chrome that enables Cross-Origin Resource Sharing working.  

* #11  
Set boolean argument to false in fnUpdate function in find() function so that every time on fnUpdate function trigger the datatable does not switch to first page.  
For example when we change radio button values in Tf Type column.  

**Note:**  
The best side of the datatables is that it can take large amount of rows and it will not overwhelm your browser while working,  
as datatbles paginate your data and consequently will render/show  your data only certain rows count chunk at each page.  
By default it paginates the data by showing 10 rows per page which can be changed to 25, 50, 100.  
