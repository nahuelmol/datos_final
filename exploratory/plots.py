
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from abss.fs import current_project

class Plot:
    def __init__(self, filename, data):
        self.pname = current_project(['project_name'])
        self.fpath = 'prs\{}\outputs\{}'.format(self.pname, filename)
        self.data  = data

    def boxplot(self):
        sns.boxplot(x=self.data)
        plt.savefig(self.fpath, dpi=300)
        plt.close()

    def histos(self, ref, kde):
        self.data = self.data.select_dtypes(include=['number'])
        sns.histplot(data=self.data, x=ref, kde=kde, bins=20)
        plt.savefig(self.fpath, dpi=300)
        plt.close()

    def hist(self):
        sns.countplot(x=self.data)
        pname = current_project(['project_name'])
        plt.savefig(self.fpath, dpi=300)
        plt.close()

    def corr_plot(self):
        numerical = self.data.select_dtypes(include=['number']).copy()
        corr_matrix = numerical.corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        plt.figure(figsize=(12,8))
        sns.heatmap(corr_matrix, cmap='coolwarm', mask=mask)
        plt.title(f"Correlation Matrix", fontsize=16, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.savefig(self.fpath, dpi=300)
        plt.close()
        return True

