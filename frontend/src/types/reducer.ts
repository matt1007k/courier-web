export type ActionMap<M extends { [Key: string]: any }> = {
	[Key in keyof M]: M[Key] extends undefined
	? {
		type: Key
	} : {
		type: Key,
		payload: M[Key]
	}
};