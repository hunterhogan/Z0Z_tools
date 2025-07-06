"""Generate PyTorch tensor windowing functions from existing windowing functions.

(AI generated docstring)

This module programmatically creates PyTorch tensor versions of windowing functions by transforming existing functions from the `windowingFunctions` module. It generates functions that return PyTorch tensors instead of NumPy arrays.

"""
from astToolkit import Be, IngredientsModule, Make, NodeTourist, parseLogicalPath2astModule, Then
from astToolkit.transformationTools import makeDictionaryFunctionDef, write_astModule
from hunterMakesPy import raiseIfNone
from pathlib import Path
import ast

packageName = 'Z0Z_tools'
moduleDestination = 'optionalPyTorch'
moduleSource = 'windowingFunctions'

pathFilenameDestination = Path(packageName, moduleDestination + '.py')

ingredientsModule = IngredientsModule()

ingredientsModule.appendPrologue(statement=Make.Assign([Make.Name('callableReturnsNDArray', ast.Store())]
			, value=Make.Call(Make.Name('TypeVar')
				, listParameters=[Make.Constant('callableReturnsNDArray')]
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
				, value=Make.Call(Make.Name('callableTarget'), listParameters=[Make.Starred(value=Make.Name('arguments'))], list_keyword=[Make.keyword(None, value=Make.Name('keywordArguments'))])
			)
		, Make.Return(Make.Call(Make.Attribute(Make.Name('torch'), 'tensor'), list_keyword=[
					Make.keyword('data', value=Make.Name('arrayTarget'))
					, Make.keyword('dtype', value=Make.Attribute(Make.Name('torch'), 'float32'))
					, Make.keyword('device', value=Make.Name('device'))
				]))
	]
	, returns=Make.Attribute(Make.Name('torch'), 'Tensor')
))

dictionaryFunctionDef: dict[str, ast.FunctionDef] = makeDictionaryFunctionDef(parseLogicalPath2astModule('.'.join([packageName, moduleSource])))  # noqa: FLY002

for callableIdentifier, astFunctionDef in dictionaryFunctionDef.items():
	if callableIdentifier.startswith('_'):
		continue

	ImaIndent = ' ' * 4
	ImaReturnsSection = f"\n{ImaIndent}Returns"
	docstringDevice = f"{ImaIndent}device : Device = torch.device(device='cpu')\n{ImaIndent}{ImaIndent}PyTorch device for tensor allocation.\n"
	docstring = Make.Expr(Make.Constant(raiseIfNone(ast.get_docstring(astFunctionDef, clean=False), errorMessage="Where's the windowing function docstring?")
						.replace('\t', ImaIndent).replace(ImaReturnsSection, docstringDevice + ImaReturnsSection)))

	ingredientsModule.imports.addImportFrom_asStr(packageName, callableIdentifier)

	argumentSpecification: ast.arguments = raiseIfNone(NodeTourist(Be.arguments, Then.extractIt).captureLastMatch(astFunctionDef))
	args: list[ast.expr] = [Make.Name(ast_arg.arg) for ast_arg in [*argumentSpecification.args, *argumentSpecification.kwonlyargs]]

	list_keyword: list[ast.keyword] = [Make.keyword('callableTarget', Make.Name(callableIdentifier))
									, Make.keyword('device', Make.Name('device'))]
	if argumentSpecification.kwarg:
		list_keyword.append(Make.keyword(None, value=Make.Name(argumentSpecification.kwarg.arg)))

	argumentSpecification.args.append(Make.arg('device', annotation=Make.BitOr.join([Make.Name('Device'), Make.Constant(None)])))
	argumentSpecification.defaults.append(Make.Constant(None))

	ingredientsModule.appendPrologue(statement=Make.FunctionDef(callableIdentifier + 'Tensor'
		, argumentSpecification
		, body=[docstring
			, Make.Assign([Make.Name('device', ast.Store())]
				, value=Make.Or.join([Make.Name('device'), Make.Call(Make.Attribute(Make.Name('torch'), 'device'), list_keyword=[Make.keyword('device', value=Make.Constant('cpu'))])])
			)
			, Make.Return(Make.Call(Make.Name('_convertToTensor'), listParameters=args, list_keyword=list_keyword))]
		, returns=Make.Attribute(Make.Name('torch'), 'Tensor')
	))

ingredientsModule.imports.addImportFrom_asStr('torch.types', 'Device')
ingredientsModule.imports.addImportFrom_asStr('typing', 'Any')
ingredientsModule.imports.addImport_asStr('torch')

write_astModule(ingredientsModule, pathFilenameDestination, packageName)

docstringModule = '"""Create PyTorch tensor windowing functions."""\n'
pathFilenameDestination.write_text(docstringModule + pathFilenameDestination.read_text())

