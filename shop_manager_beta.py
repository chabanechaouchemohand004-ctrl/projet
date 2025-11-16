"""
Gestionnaire des magasins.
Auteur: Chabane Chaouche
Numéro étudiant: 21324150  
Date: Novembre 2025
Cours: POO - Projet Blue Prince

Ce module gère toutes les interactions avec les magasins du jeu,
permettant au joueur d'échanger des pièces d'or contre des objets utiles.
"""

class ShopManager:
    """
    Gère les interactions avec les magasins et les échanges commerciaux.
    
    Cette classe permet au joueur d'acheter des objets en échange de pièces d'or.
    Elle gère la vérification des fonds, l'exécution des transactions et l'affichage
    du catalogue des produits disponibles.
    
    Attributes:
        player (Player): Référence vers l'instance du joueur
        shop_catalog (dict): Catalogue des objets disponibles à l'achat
    """
    
    def __init__(self, player):
        """
        Initialise le gestionnaire de magasin.
        
        Args:
            player: L'instance du joueur qui effectue les achats
        """
        self.player = player
        
        # Catalogue complet des objets disponibles à l'achat
        # Structure: { nom_objet: { prix, émoji, description, quantité (optionnel) } }
        self.shop_catalog = {
            'key': {
                'price': 10, 
                'emoji': '🔑',
                'description': 'Clé pour ouvrir les coffres et portes',
                'effect': 'Ouvre les serrures'
            },
            'gem': {
                'price': 25, 
                'emoji': '💎', 
                'description': 'Gemme précieuse pour acheter des pièces spéciales',
                'effect': 'Monnaie pour pièces spéciales'
            },
            'dice': {
                'price': 15, 
                'emoji': '🎲',
                'description': 'Dé à six faces pour les événements aléatoires', 
                'effect': 'Déclenche des événements spéciaux'
            },
            'steps_pack': {
                'price': 5, 
                'emoji': '👣', 
                'quantity': 10,
                'description': 'Pack de 10 pas supplémentaires',
                'effect': 'Augmente la mobilité'
            },
            'food_pack': {
                'price': 8,
                'emoji': '🍎',
                'quantity': 3, 
                'description': 'Pack de 3 fruits pour regagner des pas',
                'effect': 'Restaure 2 pas par fruit'
            }
        }
    
    def can_buy(self, item_name: str) -> bool:
        """
        Vérifie si le joueur peut acheter un objet donné.
        
        Cette méthode vérifie deux conditions :
        1. L'objet existe dans le catalogue
        2. Le joueur a assez de pièces d'or pour l'acheter
        
        Args:
            item_name: Le nom de l'objet à vérifier ('key', 'gem', etc.)
            
        Returns:
            bool: True si l'achat est possible, False sinon
            
        Example:
            >>> shop_manager.can_buy('key')
            True  # Si le joueur a au moins 10 pièces
        """
        # Vérification que l'objet existe dans le catalogue
        if item_name not in self.shop_catalog:
            return False
        
        # Vérification que le joueur a assez de pièces
        price = self.shop_catalog[item_name]['price']
        return self.player.inventory.coins.quantity >= price
    
    def get_item_price(self, item_name: str) -> int:
        """
        Récupère le prix d'un objet du catalogue.
        
        Args:
            item_name: Le nom de l'objet
            
        Returns:
            int: Le prix de l'objet, 0 si l'objet n'existe pas
        """
        if item_name in self.shop_catalog:
            return self.shop_catalog[item_name]['price']
        return 0
    
    def buy_item(self, item_name: str) -> bool:
        """
        Achète un objet du magasin et l'ajoute à l'inventaire du joueur.
        
        Cette méthode exécute toute la transaction :
        1. Vérifie si l'achat est possible
        2. Débite le prix du compte du joueur
        3. Ajoute l'objet à l'inventaire
        4. Affiche un message de confirmation
        
        Args:
            item_name: Le nom de l'objet à acheter
            
        Returns:
            bool: True si l'achat a réussi, False en cas d'échec
            
        Example:
            >>> shop_manager.buy_item('key')
            True  # Si l'achat a réussi
        """
        # Vérification préalable de la possibilité d'achat
        if not self.can_buy(item_name):
            print("💰 Pas assez de pièces pour cet achat!")
            return False
        
        # Récupération des informations de l'objet
        item_info = self.shop_catalog[item_name]
        price = item_info['price']
        emoji = item_info['emoji']
        
        # Phase 1: DÉBIT - Retrait des pièces de l'inventaire
        self.player.inventory.coins.remove(price)
        
        # Phase 2: CRÉDIT - Ajout de l'objet à l'inventaire
        success = self._give_purchased_item(item_name, item_info)
        
        if success:
            # Affichage du message de confirmation
            item_display_name = self._get_item_display_name(item_name)
            print(f"{emoji} {item_display_name} acheté pour {price} pièces d'or!")
            print(f"💰 Portefeuille restant: {self.player.inventory.coins.quantity} pièces")
            return True
        else:
            # En cas d'erreur, remboursement des pièces
            self.player.inventory.coins.add(price)
            print("❌ Erreur lors de l'achat - Transaction annulée")
            return False
    
    def _give_purchased_item(self, item_name: str, item_info: dict) -> bool:
        """
        Donne l'objet acheté au joueur selon son type.
        
        Args:
            item_name: Le nom de l'objet
            item_info: Les informations de l'objet du catalogue
            
        Returns:
            bool: True si l'objet a été correctement ajouté
        """
        try:
            if item_name == 'key':
                self.player.inventory.add_item('keys', 1)
            elif item_name == 'gem':
                self.player.inventory.add_item('gems', 1)
            elif item_name == 'dice':
                self.player.inventory.add_item('dice', 1)
            elif item_name == 'steps_pack':
                quantity = item_info['quantity']
                self.player.inventory.steps.add(quantity)
            elif item_name == 'food_pack':
                # Ajoute 3 fruits de base
                self.player.inventory.add_item('food_apple', 3)
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de l'objet: {e}")
            return False
    
    def _get_item_display_name(self, item_name: str) -> str:
        """
        Retourne le nom d'affichage formaté d'un objet.
        
        Args:
            item_name: Le nom technique de l'objet
            
        Returns:
            str: Le nom formaté pour l'affichage
        """
        display_names = {
            'key': 'Clé',
            'gem': 'Gemme', 
            'dice': 'Dé',
            'steps_pack': 'Pack de pas',
            'food_pack': 'Pack de nourriture'
        }
        return display_names.get(item_name, item_name)
    
    def display_shop(self):
        """
        Affiche le catalogue complet du magasin de manière formatée.
        
        Cette méthode présente :
        - Le titre et en-tête du magasin
        - La liste de tous les objets disponibles avec leurs prix
        - Les informations détaillées pour chaque objet
        - L'état des fonds du joueur
        - Les indicateurs visuels de ce qui est abordable
        """
        print("\n" + "=" * 60)
        print("🏪 MAGASIN - ÉCHANGEZ VOS PIÈCES CONTRE DES OBJETS UTILES")
        print("=" * 60)
        
        # Affichage du portefeuille actuel
        current_coins = self.player.inventory.coins.quantity
        print(f"💰 Votre portefeuille: {current_coins} pièces d'or")
        print("-" * 60)
        
        # Affichage du catalogue
        for item_name, info in self.shop_catalog.items():
            price = info['price']
            emoji = info['emoji']
            description = info.get('description', 'Objet mystérieux')
            
            # Indicateur visuel de possibilité d'achat
            can_afford = "🟢" if self.can_buy(item_name) else "🔴"
            
            # Nom d'affichage formaté
            display_name = self._get_item_display_name(item_name)
            
            # Affichage de la ligne produit
            print(f"{can_afford} {emoji} {display_name:.<20} {price:>3} pièces")
            print(f"    📝 {description}")
            
            # Information supplémentaire sur la quantité pour les packs
            if 'quantity' in info:
                quantity = info['quantity']
                print(f"    📦 Contient: {quantity} unités")
            
            print()  # Ligne vide pour la lisibilité
        
        print("=" * 60)
        print("🟢 Objet abordable | 🔴 Objet trop cher")
        print("=" * 60)
    
    def get_affordable_items(self) -> list:
        """
        Récupère la liste des objets que le joueur peut se permettre d'acheter.
        
        Returns:
            list: Liste des noms d'objets abordables
        """
        return [item_name for item_name in self.shop_catalog if self.can_buy(item_name)]
    
    def get_shop_statistics(self) -> dict:
        """
        Récupère des statistiques sur le magasin et la situation du joueur.
        
        Returns:
            dict: Statistiques diverses sur le magasin
        """
        total_items = len(self.shop_catalog)
        affordable_items = len(self.get_affordable_items())
        cheapest_price = min(info['price'] for info in self.shop_catalog.values())
        most_expensive_price = max(info['price'] for info in self.shop_catalog.values())
        
        return {
            'total_items': total_items,
            'affordable_items': affordable_items,
            'cheapest_price': cheapest_price,
            'most_expensive_price': most_expensive_price,
            'player_coins': self.player.inventory.coins.quantity,
            'can_afford_anything': affordable_items > 0
        }


# ============================================================================
# FONCTION DE DÉMONSTRATION
# ============================================================================

def demonstrate_shop_manager():
    """
    Fonction de démonstration du ShopManager pour tests pédagogiques.
    """
    print("🧪 DÉMONSTRATION DU SYSTÈME DE MAGASIN")
    print("=" * 50)
    
    # Note: Dans un contexte réel, on aurait une instance de Player
    class MockPlayer:
        def __init__(self):
            class MockInventory:
                class MockCoins:
                    def __init__(self):
                        self.quantity = 30
                    
                    def remove(self, amount):
                        self.quantity -= amount
                    
                    def add(self, amount):
                        self.quantity += amount
                
                def __init__(self):
                    self.coins = self.MockCoins()
                    self.steps = type('Steps', (), {'add': lambda x, y: None})()
                
                def add_item(self, item_type, quantity):
                    print(f"📦 Ajout de {quantity} {item_type} à l'inventaire")
            
            self.inventory = MockInventory()
    
    # Création des instances de test
    mock_player = MockPlayer()
    shop_manager = ShopManager(mock_player)
    
    # Affichage du magasin
    shop_manager.display_shop()
    
    # Test d'achat
    print("\n💳 TEST D'ACHAT D'UNE CLÉ:")
    shop_manager.buy_item('key')
    
    print(f"\n💰 Portefeuille après achat: {mock_player.inventory.coins.quantity} pièces")
    
    # Statistiques
    stats = shop_manager.get_shop_statistics()
    print(f"\n📊 Statistiques magasin: {stats}")


if __name__ == "__main__":
    demonstrate_shop_manager()