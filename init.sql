CREATE OR REPLACE FUNCTION transaction_check() RETURNS TRIGGER AS
$$
DECLARE
	csr CURSOR FOR SELECT * FROM transactions where demat_ac= new.dmt.account_no  ;
	port portfolio%rowtype;
BEGIN
/*dbms_output.put_line('Trigger for Transactions triggered');*/
if( new.buy == true )then
	if( dmt.Funds_Avail < (new.price* new.quantity))then
		/*dbms_output.put_line('No Enough Balance to buy '||:new.quantity|| ' shares');*/
		RAISE EXCEPTION 'Not Enough Balance to buy';
	end if;
	open csr;
	loop
		fetch csr into port;
		exit when csr%notfound;
		if (port.company_id== new.company_id)then
			update portfolio set bid_price=(( (port.bid_price*port.quantity)+(new.price * new.quantity))/(port.quantity + new.quantity)) where company_id=new.company_id and demat_ac=new.demat_ac;
			update portfolio set quantity=(port.quantity + new.quantity) where company_id=new.company_id and demat_ac=new.demat_ac; 
			update demat set funds_avail=funds_avail-(new.price* new.quantity) where demat_ac=new.demat_ac;
			update demat set funds_invested=funds_invested+(new.price* new.quantity) where demat_ac=new.demat_ac;
			return new;
		end if;
	end loop;
	insert into portfolio values(new.company_id,new.quantity,new.price,dmt.account_no);
	update demat set funds_avail=funds_avail-(new.price* new.quantity) where demat_ac=new.demat_ac;
	update demat set funds_invested=funds_avail+(new.price* new.quantity) where demat_ac=new.demat_ac;
else
	open csr;
	loop
		fetch csr into port;
		exit when csr%notfound;
		if (port.company_id== new.company_id)then
			if( port.quantity == new.quantity ) then
				delete from portfolio where company_id=new.company_id and demat_ac=new.demat_ac;
			else
				update portfolio set quantity=port.quantity - new.quantity where company_id=new.company_id and demat_ac=new.demat_ac; 
			end if;
			update demat set funds_avail=funds_avail+(new.price* new.quantity) where demat_ac=new.demat_ac;
			update demat set funds_invested=funds_invested-(new.price* new.quantity) where demat_ac=new.demat_ac;
			return new;
		end if;
	end loop;
	RAISE EXCEPTION 'Shares not found';

end if;
end;
$$ LANGUAGE PLPGSQL;

CREATE TRIGGER UPDATE_TRANSACTION_PORTFOLIO
	BEFORE INSERT ON TRANSACTIONS
	FOR EACH ROW EXECUTE PROCEDURE transaction_check();