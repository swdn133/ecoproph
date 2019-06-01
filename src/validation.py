import pickle
import matplotlib.pyplot as plt

from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric


def validation_main():
    try:
        print("Try to read model parameters...")
        fin = open('C:\\workspace\\ecoproph\\ecoproph.pckl', 'rb')
        model = pickle.load(fin)

        print("Validation begin...")
        df_cv = cross_validation(model, initial='860 days', period='60 days', horizon = '30 days')
        fig = plot_cross_validation_metric(df_cv, metric='mape', rolling_window=0.2)
        plt.savefig('C:\\workspace\\ecoproph\\validation.png', bbox_inches='tight', dpi=500)

        plt.show()

    except FileNotFoundError:
        print("No saved .pckl model found!")
        print("Create and save a model before validation.")


if __name__ == '__main__':
    splash = """\n\n
 _____ _____ _________________ ___________ _   _ 
|  ___/  __ \  _  | ___ \ ___ \  _  | ___ \ | | |
| |__ | /  \/ | | | |_/ / |_/ / | | | |_/ / |_| |
|  __|| |   | | | |  __/|    /| | | |  __/|  _  |
| |___| \__/\ \_/ / |   | |\ \\  \_/ / |   | | | |
\____/ \____/\___/\_|   \_| \_|\___/\_|   \_| |_/                                            
    \n\n              -- Validation -- \n\n"""
    print(splash)
    validation_main()        
