def group_by_attribute(attribute, df):
    if attribute[1] == "nominal":
        return df.groupby(attribute[0])
    else:
        return df.groupby(df[attribute[0]] > df[attribute[0]].mean())
