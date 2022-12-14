# cash_bills_distribution
This method allows you to distribute available cash bills between payments, you need to hand out  
The method, by the way, seeks for minimal amount of bills, that will be handed out, per each payment

## Additional Python Libraries Required:
### Pandas
<ul>
       pip install pandas
</ul>

## Descripton of method:
Method requires 2 input dictionaries, which keys and values must be integers: 
- first contains list of amounts which we want to hand out, e.g.: {0:1230, 1:450, 2:54}.  
This means that we have to hand out 3 different amounts: $1230, $450, $54
- second - is the amount of cash bills we have in stock, e.g.: {100:13, 50:100, 20:10, 10:1, 5:0}.  
This means that we have only 4 bills denominations: $100 - 13pcs, $50 - 100pcs, $20 - 10pcs, $10 - 1pcs

## Method returns:
dataframe: contains bills distribution for each amount  
dictionary: amount of used bills for each denominations   
dictionary: amount of left bills for each denominations  
dictionary: amount of needed bills, which are not available in stock, for each of denominations  
integer: sum, which is impossibly to hand out because of the lack of bills  
integer: sum, which is impossibly to hand out because of absence of needed denomination in input list  

## Example:
input <ul> bills_distribution({0:1230, 1:450, 2:54}, {100:13, 50:100, 20:10, 10:1, 5:0}) </ul>

output <ul>
### tuple, which contains:
##### df
index|sum|sum_rest|100|50|20|10|5
---|---|---|---|---|---|---|---
0|||||||
0|1230|0|12|0|1|1|0
1|450|0|1|7|0|0|0  
2|54|4|0|1|0|0|0  

##### amount of used bills for each of denominations
 {5: 0, 10: 1, 20: 1, 50: 8, 100: 13}
##### amount of left bills for each of denominations
 {5: 0, 10: 0, 20: 9, 50: 92, 100: 0}
##### amount of needed bills, which are not available in stock, for each of denominations
 {100: 0, 50: 0, 20: 0, 10: 0, 5: 0}
##### sum, which is impossibly to hand out, because of the lack of bills
 0
##### sum, which is impossibly to hand out, because of absence of needed denomination in input list
 4
 </ul>
