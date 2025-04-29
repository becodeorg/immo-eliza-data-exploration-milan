from sklearn.base import BaseEstimator, TransformerMixin


class ColumnDropper(BaseEstimator, TransformerMixin):
    """Transformer that drops specified columns from a DataFrame."""

    def __init__(self, columns_to_drop=None):
        self.columns_to_drop = columns_to_drop

    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        return x.drop(columns=self.columns_to_drop)
    
class NADropper(BaseEstimator, TransformerMixin):
    """Transformer that drops rows with NaN values in specified columns."""

    def __init__(self, subset=None):
        self.subset = subset

    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        return x.dropna(subset=self.subset)
    
class NAReplacer(BaseEstimator, TransformerMixin):
    """Transformer that replaces specified values in a DataFrame."""

    def __init__(self, column, new_value):
        self.column = column
        self.new_value = new_value

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        x_copy = x.copy()
        
        if isinstance(self.column, list):
            # Handle list
            for col in self.column:
                # if col in x_copy.columns:
                new_val = self.new_value if self.new_value != 'mean' else int(x_copy[col].mean())
                print(new_val)
                x_copy[col].fillna(new_val, inplace=True)
        else:
            #Handle single column
            # if self.column in x_copy.columns:
            new_val = self.new_value if self.new_value != 'mean' else int(x_copy[self.column].mean())
            x_copy[self.column].fillna(new_val, inplace=True)
        
        return x_copy

class DuplicateDropper(BaseEstimator, TransformerMixin):
    """Transformer that drops duplicate rows from a DataFrame."""

    def __init__(self, subset=None):
        self.subset = subset
        pass

    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        return x.drop_duplicates(self.subset)

class StringPrepare(BaseEstimator, TransformerMixin):
    """Transformer that strips whitespace & uppercase string columns in a DataFrame."""
    
    def __init__(self):
        pass
        
    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        x_transformed = x.copy()
        
        # Apply strip to string columns only
        for column in x_transformed.select_dtypes(include=['object']).columns:
            
            if x_transformed[column].isna().any():
                raise ValueError(f"Column {column} contains NaN values. Please handle them before using StringPrepare.")

            x_transformed[column] = x_transformed[column].str.strip().str.upper()
        return x_transformed
    
class BooleanTransformer(BaseEstimator, TransformerMixin):
    """Transformer that converts boolean strings to integers (True=1, False=0)."""
    
    def __init__(self):
        pass
    
    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        x_transformed = x.copy()
        
        # Convert only object columns with True/False values to int
        cols = x_transformed.select_dtypes(include=['object']).columns

        for col in cols:
            is_bool_column = x_transformed[col].isin(['TRUE', 'FALSE']).all()

            if is_bool_column:
                x_transformed[col] = x_transformed[col].map({'TRUE': 1, 'FALSE': 0})
            
        return x_transformed
    

class RoomCountCalculator(BaseEstimator, TransformerMixin):
    """Transformer that calculates and fills missing roomCount values based on other room features."""
    
    def __init__(self,):
        self.room_features = ['hasLivingRoom', 
                              'hasDiningRoom', 
                              'hasOffice', 
                              'hasDressingRoom', 
                              'hasBasement', 
                              'hasAttic']
        
    def fit(self, x, y=None):
        return self
    
    def transform(self, x):
        x_copy = x.copy()
        
        x_copy['calculated_roomCount'] = x_copy['bedroomCount'] + x_copy['bathroomCount']
        
        for feature in self.room_features:
            x_copy['calculated_roomCount'] += x_copy[feature].astype(int)
        
        # Round
        x_copy['calculated_roomCount'] = x_copy['calculated_roomCount'].round().astype(int)
        
        # Fill NaN values in roomCount with calculated values
        if 'roomCount' in x_copy.columns:
            mask = x_copy['roomCount'].isna()
            x_copy.loc[mask, 'roomCount'] = x_copy.loc[mask, 'calculated_roomCount']
        
        x_copy.drop(columns=['calculated_roomCount'], inplace=True)
        
        return x_copy