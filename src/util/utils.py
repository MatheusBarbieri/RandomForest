def group_by_attribute(attr, df):
    if attr[1] == "categorical":
        return df.groupby(attr[0])
    else:
        return df.groupby(df[attr[0]] < df[attr[0]].mean())
