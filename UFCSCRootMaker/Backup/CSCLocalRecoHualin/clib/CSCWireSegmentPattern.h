// point to IP
const int nWireGroup_1 = 14;
int w_rows_1[nWireGroup_1] = {0,0,0,1,1,2,3,3,4,4,4,5,5,5};
int w_cols_1[nWireGroup_1] = {-2,-1,0,-1,0,0,0,1,0,1,2,0,1,2};
double w_data_1[nWireGroup_1] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1};

// opposite pointting
const int nWireGroup_2 = 14;
int w_rows_2[nWireGroup_2] = {0,0,0,1,1,2,3,3,4,4,4,5,5,5};
int w_cols_2[nWireGroup_2] = {2,1,0,1,0,0,0,-1,0,-1,-2,0,-1,-2};
double w_data_2[nWireGroup_2] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1};

const int nWireGroup_3 = 13;
int w_rows_3[nWireGroup_3] = {0,0,0,1,1,2,3,3,4,4,5,5,5};
int w_cols_3[nWireGroup_3] = {-3,-2,-1,-1,0,0,0,1,1,2,1,2,3};
double w_data_3[nWireGroup_3] = {1,1,1,1,1,1,1,1,1,1,1,1,1};

const int nWireGroup_4 = 13;
int w_rows_4[nWireGroup_4] = {0,0,0,1,1,2,3,3,4,4,5,5,5};
int w_cols_4[nWireGroup_4] = {1,2,3,0,1,0,-1,0,-2,-1,-3,-2,-1};
double w_data_4[nWireGroup_4] = {1,1,1,1,1,1,1,1,1,1,1,1,1};

const int nDefinedWirePatterns = 4;
int nWGsInPatterns[nDefinedWirePatterns] = {nWireGroup_1,nWireGroup_2,nWireGroup_3,nWireGroup_4};
int patternRanks_w[nDefinedWirePatterns] = {1,3,2,4};
int* w_rows[nDefinedWirePatterns] = {w_rows_1, w_rows_3, w_rows_2, w_rows_4};
int* w_cols[nDefinedWirePatterns] = {w_cols_1, w_cols_3, w_cols_2, w_cols_4};
double* w_data[nDefinedWirePatterns] = {w_data_1, w_data_3, w_data_2, w_data_4};


// old patterns
const int nWireGroup_1_old = 14;
int w_rows_1_old[nWireGroup_1_old] = {0,0,0,1,1,2,3,3,4,4,4,5,5,5};
int w_cols_1_old[nWireGroup_1_old] = {-2,-1,0,-1,0,0,0,1,0,1,2,0,1,2};
double w_data_1_old[nWireGroup_1_old] = {1,1,1,1,1,1,1,1,1,1,1,1,1,1};

const int nDefinedWirePatterns_old = 1;
int nWGsInPatterns_old[nDefinedWirePatterns_old] = {nWireGroup_1_old};
int patternRanks_w_old[nDefinedWirePatterns_old] = {1};
int* w_rows_old[nDefinedWirePatterns_old] = {w_rows_1_old};
int* w_cols_old[nDefinedWirePatterns_old] = {w_cols_1_old};
double* w_data_old[nDefinedWirePatterns_old] = {w_data_1_old};

