CREATE OR REPLACE FUNCTION transaction_check() RETURNS TRIGGER AS
$$
DECLARE
	port portfolio%rowtype;
	dmt demat;
BEGIN
SELECT * INTO dmt FROM demat WHERE account_no = new.demat_ac;
select * into port from portfolio where company_id = new.company_id and demat_ac = new.demat_ac;
if new.buy = true then
	if (dmt."Funds_Avail") < (new.price* new.quantity) then
		RAISE EXCEPTION 'Not Enough Balance to buy';
	end if;
	if(new.price<0) then
		RAISE EXCEPTION 'InValid Price';
	End if;
	if( new.quantity <=0 )then
		RAISE EXCEPTION 'INVALID QUANTITY';
	end if;
		if port is not null then
			update portfolio set bid_price=(( (port.bid_price*port.quantity)+(new.price * new.quantity))/(port.quantity + new.quantity)) where company_id=new.company_id and demat_ac=new.demat_ac;
			update portfolio set quantity=(port.quantity + new.quantity) where company_id=new.company_id and demat_ac=new.demat_ac; 
			update demat set "Funds_Avail"="Funds_Avail"-(new.price* new.quantity) where account_no=new.demat_ac;
			update demat set "Funds_Invested"="Funds_Invested"+(new.price* new.quantity) where account_no=new.demat_ac;
			return new;
		end if;
	insert into portfolio(company_id,quantity,bid_price,demat_ac) values(new.company_id,new.quantity,new.price,dmt.account_no);
	update demat set "Funds_Avail"="Funds_Avail"-(new.price* new.quantity) where account_no=new.demat_ac;
	update demat set "Funds_Invested"="Funds_Invested"+(new.price* new.quantity) where account_no=new.demat_ac;
	return new;
else
		if port is not null then
			if( port.quantity = new.quantity ) then
				delete from portfolio where company_id=new.company_id and demat_ac=new.demat_ac;
			else
				update portfolio set quantity=port.quantity - new.quantity where company_id=new.company_id and demat_ac=new.demat_ac; 
			end if;
			update demat set "Funds_Avail"="Funds_Avail"+(new.price* new.quantity) where account_no=new.demat_ac;
			update demat set "Funds_Invested"="Funds_Invested"-(new.price* new.quantity) where account_no=new.demat_ac;
			update demat set "Funds_Invested"=0 where "Funds_Invested"<0;
			return new;
		end if;
	RAISE EXCEPTION 'Shares not found';

end if;
end;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER UPDATE_TRANSACTION_PORTFOLIO
	BEFORE INSERT ON TRANSACTIONS
	FOR EACH ROW EXECUTE PROCEDURE transaction_check();


CREATE OR REPLACE FUNCTION TRANSACTION_FILTER(opt IN int,dmt IN int,condition IN VARCHAR) 
RETURNS REFCURSOR AS 
$$ 
declare 
trans_filter  REFCURSOR;
BEGIN
	case opt
	when 1 then open trans_filter FOR SELECT  id ,timestamp , company_id ,demat_ac , buy , price  , quantity , status FROM TRANSACTIONS WHERE demat_ac = dmt and buy = true;
	when 2 then open trans_filter FOR SELECT * FROM TRANSACTIONS WHERE demat_ac = dmt and buy = false;
	when 3 then open trans_filter FOR SELECT * FROM TRANSACTIONS WHERE demat_ac = dmt and company_id=condition ;
	end case;

	return trans_filter;
end; $$ 
LANGUAGE PLPGSQL;

	
/* initialize companies*/
insert into company values
	('ITC.NS','ITC Limited','Diversified',0,0),
	('MARUTI.NS','Maruti Suzuki India Limited','Auto',0,0),
	('ULTRACEMCO.NS','UltraTech Cement Limited','Cement',0,0),
	('BAJFINANCE.NS','Bajaj Finance Limited','Finance',0,0),
	('TATASTEEL.NS','Tata Steel Limited','Steel',0,0),
	('BAJAJFINSV.NS','Bajaj Finserv Ltd.','Finance',0,0),
	('ONGC.NS','Oil and Natural Gas Corporation Limited','Petroleum',0,0),
	('COALINDIA.NS','Coal India Limited','Coal',0,0),
	('CIPLA.NS','Cipla Limited','Pharma',0,0),
	('NESTLEIND.NS','Nestlé India Limited','FnG',0,0),
	('LT.NS','Larsen & Toubro Limited','Diversified',0,0),
	('HDFCLIFE.NS','HDFC Life Insurance Company Limited','Insurance',0,0),
	('TITAN.NS','Titan Company Limited','Diversified',0,0),
	('SHREECEM.NS','Shree Cement Limited','Cement',0,0),
	('BHARTIARTL.NS','Bharti Airtel Limited','Telecom',0,0),
	('ICICIBANK.NS','ICICI Bank Limited','Banking',0,0),
	('HINDALCO.NS','Hindalco Industries Limited','Industry',0,0),
	('BRITANNIA.NS','Britannia Industries Limited','Fng',0,0),
	('KOTAKBANK.NS','Kotak Mahindra Bank Limited','Banking', 0 ,0),
	('TATACONSUM.NS','Tata Consumer Products Limited','Consumer Defensive',0,0),
	('BAJAJ-AUTO.NS','Bajaj Auto Limited','Auto',0,0);

CREATE OR REPLACE FUNCTION user_check() RETURNS TRIGGER AS
$$
DECLARE
	usr "User"%rowtype;
BEGIN
	SELECT * INTO usr FROM "User";
	if new.username NOT LIKE '.....%' then
		RAISE EXCEPTION 'INVALID USERNAME';
	end if;
	if new.name NOT LIKE '% %' then
		RAISE EXCEPTION 'Enter Full name';
	end if;

END;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER auser
	BEFORE INSERT ON "User"
	FOR EACH ROW EXECUTE PROCEDURE user_check();