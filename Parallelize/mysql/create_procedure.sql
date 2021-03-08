DELIMITER //
CREATE PROCEDURE Add_Value 
(
   IN client INT,
   IN electric_value INT
) 

BEGIN 
   INSERT INTO Counter (client_id, e_value)
   VALUES (client, electric_value);
END //
DELIMITER;








DELIMITER //
CREATE PROCEDURE Add_Total_Value 
(
   IN electric_value_total INT
) 

BEGIN 
   INSERT INTO Total (total)
   VALUES (electric_value_total);
END //


DELIMITER ;


