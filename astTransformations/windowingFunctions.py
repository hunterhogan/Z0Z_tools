from astToolkit import Be, IngredientsModule, NodeTourist, Make, parseLogicalPath2astModule, Then
from astToolkit.transformationTools import makeDictionaryFunctionDef, write_astModule
from pathlib import Path
from Z0Z_tools import raiseIfNone
import ast

packageName = 'Z0Z_tools'
moduleDestination = 'optionalPyTorch'
moduleSource = 'windowingFunctions'

pathFilenameDestination = Path(packageName, moduleDestination + '.py')

ingredientsModule = IngredientsModule()

ingredientsModule.appendPrologue(statement=Make.Assign([Make.Name('callableReturnsNDArray', ast.Store())]
			, value=Make.Call(Make.Name('TypeVar')
				, args=[Make.Constant('callableReturnsNDArray')]
				, list_keyword=[Make.keyword('bound', Make.Subscript(Make.Name('Callable'), Make.Tuple([Make.Constant(...), Make.Name('WindowingFunction')])))])))
ingredientsModule.imports.addImportFrom_asStr('collections.abc', 'Callable')
ingredientsModule.imports.addImportFrom_asStr('typing', 'TypeVar')
ingredientsModule.imports.addImportFrom_asStr('Z0Z_tools', 'WindowingFunction')

ingredientsModule.appendPrologue(statement=Make.FunctionDef('_convertToTensor'
	, Make.arguments(vararg=Make.arg('arguments', annotation=Make.Name('Any'))
		, kwonlyargs=[Make.arg('callableTarget', annotation=Make.Name('callableReturnsNDArray')), Make.arg('device', annotation=Make.Name('Device'))]
		, kw_defaults=[None, None]
		, kwarg=Make.arg('keywordArguments', annotation=Make.Name('Any'))
	)
	, body=[Make.Assign([Make.Name('arrayTarget', ast.Store())]
				, value=Make.Call(Make.Name('callableTarget'), args=[Make.Starred(value=Make.Name('arguments'))], list_keyword=[Make.keyword(arg=None, value=Make.Name('keywordArguments'))])
			)
		, Make.Return(Make.Call(Make.Attribute(Make.Name('torch'), 'tensor'), list_keyword=[
					Make.keyword('data', value=Make.Name('arrayTarget'))
					, Make.keyword('dtype', value=Make.Attribute(Make.Name('torch'), 'float32'))
					, Make.keyword('device', value=Make.Name('device'))
				]))
	]
	, returns=Make.Attribute(Make.Name('torch'), 'Tensor')
))

dictionaryFunctionDef = makeDictionaryFunctionDef(parseLogicalPath2astModule('.'.join([packageName, moduleSource])))

for callableIdentifier, astFunctionDef in dictionaryFunctionDef.items():
	if callableIdentifier.startswith('_'): continue

	ingredientsModule.imports.addImportFrom_asStr(packageName, callableIdentifier)

	findThis = Be.arguments
	doThat = Then.extractIt
	argumentSpecification = raiseIfNone(NodeTourist(findThis, doThat).captureLastMatch(astFunctionDef))
	args: list[ast.expr] = []
	for ast_arg in [*argumentSpecification.args, *argumentSpecification.kwonlyargs]:
		args.append(Make.Name(ast_arg.arg))

	list_keyword: list[ast.keyword] = [Make.keyword('callableTarget', Make.Name(callableIdentifier))
									, Make.keyword('device', Make.Name('device'))]
	if argumentSpecification.kwarg:
		list_keyword.append(Make.keyword(arg=None, value=Make.Name(argumentSpecification.kwarg.arg)))

	argumentSpecification.args.append(Make.arg('device', annotation=Make.Name('Device')))
	argumentSpecification.defaults.append(Make.Call(Make.Attribute(Make.Name('torch'), 'device'), list_keyword=[Make.keyword('device', value=Make.Constant('cpu'))]))

	ingredientsModule.appendPrologue(statement=Make.FunctionDef(callableIdentifier + 'Tensor'
		, args=argumentSpecification
		, body=[Make.Return(Make.Call(Make.Name('_convertToTensor'), args=args, list_keyword=list_keyword))]
		, returns=Make.Attribute(Make.Name('torch'), 'Tensor')
	))

ingredientsModule.imports.addImportFrom_asStr('torch.types', 'Device')
ingredientsModule.imports.addImportFrom_asStr('typing', 'Any')
ingredientsModule.imports.addImport_asStr('torch')

write_astModule(ingredientsModule, pathFilenameDestination, packageName)
