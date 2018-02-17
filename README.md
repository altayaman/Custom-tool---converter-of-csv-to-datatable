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
python csv_to_redshift_v4.1.py -f <file path> -t <table name> -s <schema name>  
```
\<file path\> - csv file path you need to insert into db.  
\<table name\> - table name that needs to be created to persist csv file data. if not passed, csv file name will be taken as table name.  
\<schema name\> - schema name where table need to be created. if not passed, default will be taken as schema name. default schema name needs to be set in 'DB credentials' section below.  

* b)  
After script is launched, it will start analyzing csv file to get column names and column data types.  
Once analysis is complete, brief columns summary can/will be printed,  
where original column names and thir types are shown in 'column names' and 'column types' respectively.  




Features:  
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
#11  
Set boolean argument to false in fnUpdate function in find() function so that every time on fnUpdate function trigger the datatable does not switch to first page.  
For example when we change radio button values in Tf Type column.  
Note:  
The best side of the datatables is that it can take large amount of rows and it will not overwhelm your browser while working,  
as datatbles paginate your data and consequently will render/show  your data only certain rows count chunk at each page.  
By default it paginates the data by showing 10 rows per page which can be changed to 25, 50, 100.  
