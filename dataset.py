class Dataset:
    def __init__(self,token_id):
        self.token_id = token_id
        self.number_of_token_creation_of_creator = 1
    
    def set_mint_count_per_week(self,mint_count_per_week):
        self.mint_count_per_week = mint_count_per_week

    def set_burn_count_per_week(self,burn_count_per_week):
        self.burn_count_per_week = burn_count_per_week

    def set_mint_ratio(self,mint_ratio):
        self.mint_ratio = mint_ratio

    def set_swap_ratio(self,swap_ratio):
        self.swap_ratio = swap_ratio

    def set_burn_ratio(self,burn_ratio):
        self.burn_ratio = burn_ratio
        
    def set_mint_mean_period(self,mint_mean_period):
        self.mint_mean_period = mint_mean_period

    def set_swap_mean_period(self,swap_mean_period):
        self.swap_mean_period = swap_mean_period

    def set_burn_mean_period(self,burn_mean_period):
        self.burn_mean_period = burn_mean_period

    def set_swap_in_per_week(self,swap_in_per_week):
        self.swap_in_per_week = swap_in_per_week

    def set_swap_out_per_week(self,swap_out_per_week):
        self.swap_out_per_week = swap_out_per_week

    def set_swap_rate(self,swap_rate):
        self.swap_rate = swap_rate

    def set_lp_avg(self,lp_avg):
        self.lp_avg = lp_avg

    def set_lp_std(self,lp_std):
        self.lp_std = lp_std
    
    def set_lp_creator_holding_ratio(self,lp_creator_holding_ratio):
        self.lp_creator_holding_ratio = lp_creator_holding_ratio

    def set_lp_lock_ratio(self,lp_lock_ratio):
        self.lp_lock_ratio = lp_lock_ratio

    def set_token_burn_ratio(self,token_burn_ratio):
        self.token_burn_ratio = token_burn_ratio
    
    def set_token_creator_holding_ratio(self,token_creator_holding_ratio):
        self.token_creator_holding_ratio = token_creator_holding_ratio
    
    

    def to_dict(self) -> dict:
        dataset = {}
        dataset['mint_count_per_week'] = self.mint_count_per_week
        dataset['burn_count_per_week'] = self.burn_count_per_week
        dataset['mint_ratio'] = self.mint_ratio
        dataset['swap_ratio'] = self.swap_ratio
        dataset['brun_ratio'] = self.burn_ratio
        dataset['mint_mean_peariod'] = self.mint_mean_period
        dataset['swap_mean_period'] = self.swap_mean_period
        dataset['burn_mean_period'] = self.burn_mean_period
        dataset['swap_in_per_week'] = self.swap_in_per_week
        dataset['swap_out_per_week'] = self.swap_out_per_week
        dataset['swap_rate'] = self.swap_rate
        dataset['lp_avg'] = self.lp_avg
        dataset['lp_std'] = self.lp_std
        dataset['lp_creator_holding_ratio'] = self.lp_creator_holding_ratio
        dataset['lp_lock_ratio'] = self.lp_lock_ratio
        dataset['token_burn_ratio'] = self.token_burn_ratio
        dataset['token_creator_holding_ratio'] = self.token_creator_holding_ratio
        dataset['number_of_token_creation_of_creator'] = self.number_of_token_creation_of_creator
        return dataset


