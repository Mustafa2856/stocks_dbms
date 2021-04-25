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

	
