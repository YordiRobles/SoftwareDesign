import unittest
from src.models.character import Character
from src.models.tank import TankCharacter

class TestTankCharacter(unittest.TestCase):
   
    def test_only_percent_reduction(self):
        """Test que el daño es reducido un 25% correctamente."""
        tank = TankCharacter(name="Tank", reduction_percent=0.25, flat_reduction=0)
        tank.take_damage(40)  # 40 * (1 - 0.25) = 30
        self.assertEqual(tank.health, 70)

    def test_only_flat_reduction(self):
        """Test donde el daño sufre una reducción plana."""
        tank = TankCharacter(name="Tank", reduction_percent=0.0, flat_reduction=7)
        tank.take_damage(20)  # 20 - 7 = 13
        self.assertEqual(tank.health, 87)

    def test_order_percent_then_flat(self):
        """Test donde el daño sufre reducción porcentual y luego una reducción plana."""
        tank = TankCharacter(name="Tank", reduction_percent=0.50, flat_reduction=3)
        
        # Valida la reducción porcentual
        after_percent = tank.percent_reduced(20)
        self.assertEqual(after_percent, 10)

        # Valida la reducción plana
        after_flat = tank.flat_reduced(after_percent)
        self.assertEqual(after_flat, 7)

        # Valida el daño final aplicado
        tank.take_damage(20)
        self.assertEqual(tank.health, 93)

    def test_flat_clamped_to_zero(self):
        """Test donde la reducción plana supera el daño a recibir."""
        tank = TankCharacter(name="Tank", reduction_percent=0.0, flat_reduction=10)
        tank.take_damage(5)
        self.assertEqual(tank.health, 100)

    def test_percent_100_immunity(self):
        """Test donde la reducción porcentual es del 100%."""
        tank = TankCharacter(name="Tank", reduction_percent=1.0, flat_reduction=0)
        tank.take_damage(999)
        self.assertEqual(tank.health, 100)

    def test_zero_and_negative_damage_no_effect(self):
        """Test que daños cero o negativos no afectan la salud."""
        tank = TankCharacter(name="Tank", reduction_percent=0.30, flat_reduction=3)
        tank.take_damage(0)
        self.assertEqual(tank.health, 100)
        tank.take_damage(-10)
        self.assertEqual(tank.health, 100)

    def test_dead_does_not_process_further_hits(self):
        """Test donde se verifica que un tanque muerto no recibe más daño."""
        tank = TankCharacter(name="Tank", reduction_percent=0.0, flat_reduction=0)
        
        #Valida que el personaje muere
        tank.take_damage(150)
        self.assertEqual(tank.health, 0)
        self.assertFalse(tank.is_alive)

        # Intenta golpear nuevamente
        tank.take_damage(50)
        self.assertEqual(tank.health, 0)
        self.assertFalse(tank.is_alive)

    def test_multiple_hits_sequence(self):
        """Test que simula múltiples golpes y verifica la salud tras cada uno."""
        tank = TankCharacter(name="Tank", reduction_percent=0.20, flat_reduction=2)
        # Valida el estado después del primer golpe
        tank.take_damage(15)
        self.assertEqual(tank.health, 90)
        
        # Valida el estado después del segundo golpe
        tank.take_damage(10)
        self.assertEqual(tank.health, 84)

        # Valida el estado después del tercer golpe
        tank.take_damage(3)
        self.assertEqual(tank.health, 84)

    def test_param_sanitization_bounds(self):
        """Test donde los parámetros de reducción se sanitizan correctamente."""
        tank = TankCharacter(name="Tank", reduction_percent=-0.5, flat_reduction=-10)
        tank.take_damage(10)
        self.assertEqual(tank.health, 90)

    def test_compare_with_normal_character(self):
        """Test que compara el daño recibido por un Character normal y un TankCharacter."""
        c = Character(name="Peon", health=50)
        # Valida el daño que recibe el Character normal
        c.take_damage(20)  # 50 -> 30
        self.assertEqual(c.health, 30)

        tank = TankCharacter(name="Tank", health=50, reduction_percent=0.25, flat_reduction=5)
        # Valida el daño que recibe el Tank Character
        tank.take_damage(20)
        self.assertEqual(tank.health, 40)