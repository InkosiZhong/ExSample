import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style(style='darkgrid')
raw_data = pd.DataFrame({
    'Instances Found' : [100, 1000, 2000, 5000, 10000],
    'random' : [439, 3689, 7670, 20152, 40437],
    '2' : [436, 3547, 7187, 19132, 39402],
    '16' : [395, 2736, 5707, 14644, 32369],
    '16 (random+)' : [343, 2613, 4962, 13190, 28412],
    #'128' : [275, 2788, 5218, 12829, 29020],
    '1024' : [302, 2820, 5340, 11610, 23559],
    '1024 (random+)' : [326, 2749, 4996, 10514, 20496],
})

data = pd.melt(raw_data, ['Instances Found'], var_name='Methods', value_name='Frame Sampled')
fig, ax = plt.subplots()
sns.lineplot(y='Instances Found', x='Frame Sampled', hue='Methods', data=data, ax=ax)
ax.set_title('bicycle@Archie')
max_ratio, ann_i = 0, 0
for i, (y, x1, x2) in enumerate(zip(raw_data['Instances Found'], raw_data['random'], raw_data['1024'])):
    ratio = x1 / x2
    if ratio > max_ratio:
        max_ratio = ratio
        ann_i = i
ax.annotate('', xy=(raw_data['1024'][ann_i], raw_data['Instances Found'][ann_i]), 
            xytext=(raw_data['random'][ann_i], raw_data['Instances Found'][ann_i]), 
            arrowprops=dict(color='black', arrowstyle="<->"))
ax.text((raw_data['1024'][ann_i] + raw_data['random'][ann_i]) / 2, 
    raw_data['Instances Found'][ann_i], 
    f'{max_ratio:.2f}x', horizontalalignment='center', verticalalignment='center',
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

plt.savefig('src/plot.png', dpi=300, bbox_inches='tight')