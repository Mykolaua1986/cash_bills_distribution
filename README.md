# cash_bills_distribution
This method allows you to distribute available cash bills between array of amounts you need to hand out
the method, by the way, seeks for minimal amount of bills that will be handed out per each payment

##Additional Python Libraries Required:
<ul>
 <li>Pandas</li>
  
       pip install pandas
</ul>

## descripton of method
Method requires 2 input dictionaries which keys and values must be integers: 
- first contains list of amounts which we want to hand out, e.g.: {0:1230, 1:450, 2:54}.
This mean that we have to hand out 3 different amounts: $1230, $450, $54
- second - is the amount of cash bills we have in stock, e.g.: {100:13, 50:100, 20:10, 10:1, 5:0}
This means that we have only 4 bills denominations: $100 - 13pcs, $50 - 100pcs, $20 - 10pcs, $10 - 1pcs

## method returns:
dataframe: cantains bills distribution for each amount
dictionary: amount of used bills for each denominations 
dictionary: amount of left bills for each denominations 
dictionary: amount of needed bills, which are not available in stock, for each denominations 
integer: sum, which is impossibly to hand out because of the lack of bills
integer: sum, which is impossibly to hand out because of absence of needed denomination in input list
