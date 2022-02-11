CREATE DEFINER = CURRENT_USER TRIGGER `Motorizadas`.`compra_AFTER_INSERT` AFTER INSERT ON `compra` FOR EACH ROW
BEGIN
	UPDATE motorizadas SET  stock = stock - NEW.quantidade
    WHERE motorizadas.idmotorizada = NEW.compra.idmotorizada;
END