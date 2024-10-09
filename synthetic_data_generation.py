from scipy.stats import gaussian_kde

sample = pd.read_csv('sample.csv') # load the sample data that you will use to generate new data
df = pd.read_csv('df.csv') # load the dataset that you want to generate new columns for 
n_train = df.shape[0]

kde = gaussian_kde(sample[["col"]])
df["col"] = kde.resample(n_train).flatten().astype(int)