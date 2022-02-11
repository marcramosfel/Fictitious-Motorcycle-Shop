CREATE DEFINER = CURRENT_USER TRIGGER `Motorizadas`.`compra_AFTER_DELETE` AFTER DELETE ON `compra` FOR EACH ROW
BEGIN
	UPDATE motorizadas SET stock = stock + OLD.quantidade
    WHERE motorizadas.idmotorizada = OLD.compra.idmotorizada;

END