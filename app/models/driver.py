class Driver:
    """
    Represents a Formula 1 driver with attributes and methods for fantasy F1 game management.
    """
    
    def __init__(self, id, name, number, team, nationality, price, season=None):
        """
        Initialize a Driver instance.
        
        Args:
            id (int): Unique identifier for the driver
            name (str): Driver's full name
            number (int): Driver's race number
            team (str): Team name
            nationality (str): Driver's nationality
            price (float): Driver's price in fantasy game
            season (int, optional): Current F1 season
        """
        self.id = id
        self.name = name
        self.number = number
        self.team = team
        self.nationality = nationality
        self.price = price
        self.season = season
        
        # Performance metrics
        self.season_points = 0
        self.wins = 0
        self.podiums = 0
        self.pole_positions = 0
        
        # Calculated metrics
        self.reliability = 0.0
        self.consistency = 0.0
        self.average_position = 0.0
        
        # Recent race data
        self.last_race_position = None
        self.last_race_points = 0
        
        # Race history for calculations
        self.stats = {
            'races_completed': 0,
            'races_dnf': 0,
            'points_history': [],
            'position_history': [],
            'total_races': 0
        }
    
    def add_points(self, points):
        """
        Add points to the driver's season total.
        
        Args:
            points (int/float): Points to add
        """
        self.season_points += points
        self.stats['points_history'].append(points)
    
    def set_race_result(self, position, points, dnf=False):
        """
        Set the result of a race for the driver.
        
        Args:
            position (int): Finishing position in the race
            points (int/float): Points earned in the race
            dnf (bool): Whether the driver did not finish (DNF)
        """
        self.last_race_position = position
        self.last_race_points = points
        
        self.stats['position_history'].append(position)
        self.stats['total_races'] += 1
        
        if dnf:
            self.stats['races_dnf'] += 1
        else:
            self.stats['races_completed'] += 1
        
        # Update podium and points
        if position and position <= 3:
            self.podiums += 1
        
        if position == 1:
            self.wins += 1
        
        self.add_points(points)
        self.calculate_reliability()
        self.calculate_consistency()
    
    def add_pole_position(self):
        """Increment the pole position counter."""
        self.pole_positions += 1
    
    def calculate_reliability(self):
        """
        Calculate driver reliability based on completion rate.
        
        Reliability is calculated as the percentage of races completed.
        Returns a value between 0.0 and 1.0.
        """
        if self.stats['total_races'] > 0:
            self.reliability = (
                self.stats['races_completed'] / self.stats['total_races']
            )
        return self.reliability
    
    def calculate_consistency(self):
        """
        Calculate driver consistency based on position variance.
        
        Consistency is calculated using the inverse of the coefficient of variation.
        Higher consistency means more stable results.
        Returns a value between 0.0 and 1.0.
        """
        if not self.stats['position_history'] or len(self.stats['position_history']) < 2:
            self.consistency = 0.0
            return self.consistency
        
        positions = self.stats['position_history']
        mean_position = sum(positions) / len(positions)
        
        # Calculate variance
        variance = sum((x - mean_position) ** 2 for x in positions) / len(positions)
        
        # Calculate standard deviation
        std_dev = variance ** 0.5
        
        # Avoid division by zero
        if mean_position == 0:
            self.consistency = 0.0
        else:
            # Coefficient of variation (std_dev / mean)
            cv = std_dev / mean_position
            # Convert to consistency score (inverse, normalized)
            # Lower CV = higher consistency (score closer to 1)
            self.consistency = max(0.0, 1.0 - (cv / 10.0))
        
        return self.consistency
    
    def get_average_position(self):
        """
        Calculate and return the average finishing position.
        
        Returns:
            float: Average position or None if no races completed
        """
        if not self.stats['position_history']:
            self.average_position = 0.0
            return self.average_position
        
        self.average_position = (
            sum(self.stats['position_history']) / len(self.stats['position_history'])
        )
        return self.average_position
    
    def to_dict(self):
        """
        Convert driver instance to dictionary representation.
        
        Returns:
            dict: Dictionary containing all driver attributes and statistics
        """
        return {
            'id': self.id,
            'name': self.name,
            'number': self.number,
            'team': self.team,
            'nationality': self.nationality,
            'price': self.price,
            'season': self.season,
            'season_points': self.season_points,
            'wins': self.wins,
            'podiums': self.podiums,
            'pole_positions': self.pole_positions,
            'reliability': round(self.reliability, 3),
            'consistency': round(self.consistency, 3),
            'average_position': round(self.get_average_position(), 2),
            'last_race_position': self.last_race_position,
            'last_race_points': self.last_race_points,
            'stats': {
                'races_completed': self.stats['races_completed'],
                'races_dnf': self.stats['races_dnf'],
                'total_races': self.stats['total_races'],
                'points_history': self.stats['points_history'],
                'position_history': self.stats['position_history']
            }
        }
    
    def __repr__(self):
        """String representation of the Driver instance."""
        return (
            f"Driver(id={self.id}, name='{self.name}', "
            f"number={self.number}, team='{self.team}', "
            f"points={self.season_points})"
        )
