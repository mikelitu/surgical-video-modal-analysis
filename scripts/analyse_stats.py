import numpy as np


def print_stats(stats: dict[str, np.ndarray], stat_name: str):

    print(f"------------ {stat_name.capitalize()} --------------\n")
    analysing_func = {"mean": np.mean, "std": np.std, "max": np.max, "min": np.min}
    for func_name, func in analysing_func.items():
        print(f"* {func_name.capitalize()} *")
        print(f"\tPhantom: {round(func(stats['phantom']), 3)}")
        print(f"\tReal: {round(func(stats['real']), 3)}")
        print(f"\tAll: {round(func(stats['all']), 3)}\n")

    # print(f"---------------------- {stat_name.capitalize()} ---------------------")
    # print(f"* Mean *")
    # print(f"\tPhantom: {round(np.mean(stats['phantom']), 3)}")
    # print(f"\tReal: {round(np.mean(stats['real']), 3)}")
    # print(f"\tAll: {round(np.mean(stats['all']), 3)}")
    # print(f"* Std *")
    # print(f"\tPhantom: {np.std(stats['phantom'])}")
    # print(f"\tReal: {np.std(stats['real'])}")
    # print(f"\tAll: {np.std(stats['all'])}")
    # print(f"* Maximum - Minimum *")
    # print(f"\tPhantom: {round(np.max(stats['phantom']), 3)} - {round(np.min(stats['phantom']), 3)}")
    # print(f"\tReal: {np.max(stats['real'])} - {np.min(stats['real'])}")
    # print(f"\tAll: {np.max(stats['all'])} - {np.min(stats['all'])}")
    



def main():
    phantom_results = {
        "cross_correlation": [0.9000969537635068, 0.5577427757017187, 0.274173999539308, 0.23541464147799712, 0.5032355036307109, 0.8393382388774538, 0.6321430942884774, 0.4586579878159971, 0.7406337276935269, 0.6220283052602622, 0.8814782444375608, 0.7117296639791724, 0.9069909779305804, 0.8033315169310927],
        "rmse": [0.38338316412443585, 0.9072410419310264, 1.1641534806438572, 1.2295577873755237, 0.991686682127292, 0.5632151618423584, 0.857477000765114, 1.0381417331770542, 0.7004422797745817, 0.8275479555717481, 0.45790271646999353, 0.7189100401566064, 0.373917127394454, 0.5660242806009469],
        "mae": [0.280368182828039, 0.7229588821193446, 0.947595720761756, 0.8145030995079612, 0.8928338479567048, 0.4070228430448777, 0.5990124936484468, 0.8392119353211899, 0.5755213931159615, 0.6545250772688904, 0.3771353418100333, 0.5544416997791148, 0.2785543352284305, 0.41039007824788176],
        "mape": [49.87405901981194, 111.8061580380459, 121.15591615897807, 156.87647268308316, 204.2202609553117, 146.6350417978512, 147.96259211262586, 198.19643164516242, 72.19767216682732, 199.40999141752937, 63.15954776543832, 95.04166057739874, 51.4525521721665, 72.09410372120429],
        "cosine": [0.9263527207677051, 0.5881106754454828, 0.3210944014329697, 0.24281206716460577, 0.5072589571064527, 0.8413718672163819, 0.6322291315215843, 0.4586842773829368, 0.7511783555576651, 0.6535537216387935, 0.8939667308890074, 0.7356662762717932, 0.9300700540496639, 0.8397327000296798]
    }

    real_results = {
        "cross_correlation": [0.7696293618601713, 0.49670528394763314, 0.5487698900476421, 0.4870724183786345, 0.5220967797429507],
        "rmse": [0.6756489313621276, 0.9964856485693118, 0.9461788252663172, 0.9549266838091566, 0.9716199923813471],
        "mae": [0.46439804115667593, 0.7000318517440478, 0.589715910441938, 0.7789923898493818, 0.7161295419123861],
        "mape": [250.3543267536965, 113.40406290339811, 83.67062363266623, 219.78907293495146, 270.1386303170904],
        "cosine": [0.7717185504274211, 0.49425807383608833, 0.5511406630690037, 0.5398337446961649, 0.5211297089656409]
    }
    
    for key in phantom_results.keys():
        p_results = phantom_results[key]
        r_results = real_results[key]
        all_results = np.concatenate((p_results, r_results))

        stats = {
            "phantom": p_results,
            "real": r_results,
            "all": all_results
        }

        print_stats(stats=stats, stat_name=key)

if __name__ == "__main__":
    main()